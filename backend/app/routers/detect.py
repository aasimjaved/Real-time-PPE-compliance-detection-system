import numpy as np
import cv2
from fastapi import APIRouter, UploadFile, File

from app.detection import detector
from app.config import settings
from app.schemas import DetectResponse, Detection as DetectionSchema

router = APIRouter(prefix="/api/detect", tags=["detect"])


@router.post("", response_model=DetectResponse)
async def detect_image(file: UploadFile = File(...)):
    """Run PPE detection on a single uploaded image. Useful for quick testing
    and for spot-checking photos (e.g. a supervisor's phone photo of a site)."""
    contents = await file.read()
    npimg = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    detections = detector.infer(frame)
    annotated = detector.annotate(frame, detections)
    b64 = detector.frame_to_b64(annotated)

    violation_count = sum(1 for d in detections if d.class_name in settings.VIOLATION_CLASSES)

    return DetectResponse(
        detections=[
            DetectionSchema(class_name=d.class_name, confidence=d.confidence, bbox=d.bbox)
            for d in detections
        ],
        violation_count=violation_count,
        compliant=violation_count == 0,
        annotated_image_b64=b64,
    )
