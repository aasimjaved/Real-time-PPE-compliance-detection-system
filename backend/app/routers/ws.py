"""
Live camera loop: reads frames from a camera source (webcam index, video file,
or RTSP URL), runs YOLO PPE detection on each frame, streams annotated JPEG
frames + violation events to every connected dashboard over WebSocket, and
persists debounced violations to the database with alert dispatch.
"""
import asyncio
import datetime as dt
import os
from collections import defaultdict, deque

import cv2
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models
from app.detection import detector
from app.websocket_manager import manager
from app.alerts import dispatch_alerts
from app.config import settings

router = APIRouter()

# Tracks how many consecutive frames each (camera, violation_type) has been
# seen, and the last time it was logged, for debouncing + cooldown.
_streak: dict[tuple[str, str], int] = defaultdict(int)
_last_logged: dict[tuple[str, str], dt.datetime] = {}


def _resolve_source(source: str):
    """Webcam index ('0'), video file path, or RTSP/HTTP stream URL."""
    if source.isdigit():
        return int(source)
    return source


async def _process_violations(db: Session, camera_id: str, camera_name: str, detections):
    now = dt.datetime.utcnow()
    for det in detections:
        if det.class_name not in settings.VIOLATION_CLASSES:
            continue
        key = (camera_id, det.class_name)
        _streak[key] += 1

        if _streak[key] < settings.VIOLATION_FRAME_THRESHOLD:
            continue

        last = _last_logged.get(key)
        if last and (now - last).total_seconds() < settings.VIOLATION_COOLDOWN_SECONDS:
            continue

        violation = models.Violation(
            camera_id=int(camera_id) if camera_id.isdigit() else None,
            violation_type=det.class_name,
            confidence=det.confidence,
            bbox_x1=det.bbox[0], bbox_y1=det.bbox[1],
            bbox_x2=det.bbox[2], bbox_y2=det.bbox[3],
            timestamp=now,
        )
        db.add(violation)
        db.commit()
        db.refresh(violation)

        alert_results = dispatch_alerts(det.class_name, camera_name, det.confidence)
        for r in alert_results:
            db.add(models.AlertLog(violation_id=violation.id, channel=r["channel"], status=r["status"]))
        db.commit()

        _last_logged[key] = now
        await manager.broadcast(camera_id, {
            "type": "violation",
            "violation_type": det.class_name,
            "confidence": det.confidence,
            "timestamp": now.isoformat(),
        })

    # decay streaks for classes not seen this frame
    seen_classes = {d.class_name for d in detections}
    for key in list(_streak):
        cam_id, cls = key
        if cam_id == camera_id and cls not in seen_classes:
            _streak[key] = 0


async def _camera_loop(camera_id: str, source: str, camera_name: str):
    cap = cv2.VideoCapture(_resolve_source(source))
    if not cap.isOpened():
        await manager.broadcast(camera_id, {"type": "error", "message": f"Could not open source: {source}"})
        return

    db = SessionLocal()
    try:
        while camera_id in manager.active:
            ok, frame = cap.read()
            if not ok:
                # loop video files; for live streams, try to reconnect
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            detections = detector.infer(frame)
            annotated = detector.annotate(frame, detections)
            b64 = detector.frame_to_b64(annotated)

            await _process_violations(db, camera_id, camera_name, detections)

            await manager.broadcast(camera_id, {
                "type": "frame",
                "image": b64,
                "detections": [
                    {"class_name": d.class_name, "confidence": d.confidence, "bbox": d.bbox}
                    for d in detections
                ],
            })
            await asyncio.sleep(0.03)  # ~30fps cap, tune per hardware
    finally:
        cap.release()
        db.close()


@router.websocket("/ws/live/{camera_id}")
async def live_feed(websocket: WebSocket, camera_id: str, source: str = "0", name: str = "Camera"):
    await manager.connect(camera_id, websocket)
    loop_task = None
    try:
        # Only spin up one capture loop per camera even with multiple viewers
        if len(manager.active.get(camera_id, [])) == 1:
            loop_task = asyncio.create_task(_camera_loop(camera_id, source, name))
        while True:
            await websocket.receive_text()  # keep-alive / future control messages
    except WebSocketDisconnect:
        manager.disconnect(camera_id, websocket)
