import datetime as dt
from typing import Optional, List

from pydantic import BaseModel, ConfigDict


class CameraCreate(BaseModel):
    name: str
    location: Optional[str] = None
    source: str
    active: bool = True


class CameraOut(CameraCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: dt.datetime


class Detection(BaseModel):
    class_name: str
    confidence: float
    bbox: List[float]   # [x1, y1, x2, y2]


class DetectResponse(BaseModel):
    detections: List[Detection]
    violation_count: int
    compliant: bool
    annotated_image_b64: Optional[str] = None


class ViolationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    camera_id: Optional[int]
    violation_type: str
    confidence: float
    snapshot_path: Optional[str]
    timestamp: dt.datetime
    resolved: bool


class StatsSummary(BaseModel):
    total_violations: int
    violations_today: int
    compliance_rate_24h: float
    violations_by_type: dict
    violations_by_camera: dict
    trend_last_7_days: List[dict]
