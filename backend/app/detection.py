"""
Thin wrapper around an Ultralytics YOLO model that turns raw frames into
structured PPE detections, and draws the annotated frame used by the
live dashboard.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
from typing import List

import cv2
import numpy as np
from ultralytics import YOLO

from app.config import settings


@dataclass
class Detection:
    class_name: str
    confidence: float
    bbox: List[float]  # x1, y1, x2, y2


VIOLATION_COLOR = (0, 0, 255)     # red   (BGR)
COMPLIANT_COLOR = (0, 200, 0)     # green
NEUTRAL_COLOR = (200, 200, 0)


class PPEDetector:
    def __init__(self, model_path: str = settings.MODEL_PATH):
        self.model = YOLO(model_path)
        # If the loaded model wasn't trained on the PPE class set (e.g. the
        # stock COCO yolov8n.pt fallback), we still run it so the app works
        # out of the box, but violation logic is skipped for unknown classes.
        self.class_names = self.model.names

    def infer(self, frame: np.ndarray) -> List[Detection]:
        results = self.model.predict(
            frame,
            conf=settings.CONFIDENCE_THRESHOLD,
            iou=settings.IOU_THRESHOLD,
            verbose=False,
        )[0]

        detections: List[Detection] = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            name = self.class_names.get(cls_id, str(cls_id)) if isinstance(self.class_names, dict) else self.class_names[cls_id]
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            detections.append(Detection(class_name=name, confidence=conf, bbox=[x1, y1, x2, y2]))
        return detections

    @staticmethod
    def annotate(frame: np.ndarray, detections: List[Detection]) -> np.ndarray:
        annotated = frame.copy()
        for det in detections:
            x1, y1, x2, y2 = map(int, det.bbox)
            if det.class_name in settings.VIOLATION_CLASSES:
                color = VIOLATION_COLOR
            elif det.class_name in {"Hardhat", "Safety Vest", "Mask"}:
                color = COMPLIANT_COLOR
            else:
                color = NEUTRAL_COLOR
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)
            label = f"{det.class_name} {det.confidence:.2f}"
            (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(annotated, (x1, y1 - th - 8), (x1 + tw + 4, y1), color, -1)
            cv2.putText(annotated, label, (x1 + 2, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        return annotated

    @staticmethod
    def frame_to_b64(frame: np.ndarray) -> str:
        ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        if not ok:
            return ""
        return base64.b64encode(buf).decode("utf-8")


# Singleton instance shared across the app
detector = PPEDetector()
