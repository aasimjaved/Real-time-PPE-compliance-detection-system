import datetime as dt

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=True)
    source = Column(String, nullable=False)   # RTSP URL, video file path, or "0" for webcam
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=dt.datetime.utcnow)

    violations = relationship("Violation", back_populates="camera")


class Violation(Base):
    __tablename__ = "violations"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=True)
    violation_type = Column(String, nullable=False)   # e.g. "NO-Hardhat"
    confidence = Column(Float, nullable=False)
    bbox_x1 = Column(Float)
    bbox_y1 = Column(Float)
    bbox_x2 = Column(Float)
    bbox_y2 = Column(Float)
    snapshot_path = Column(String, nullable=True)
    timestamp = Column(DateTime, default=dt.datetime.utcnow, index=True)
    resolved = Column(Boolean, default=False)

    camera = relationship("Camera", back_populates="violations")


class AlertLog(Base):
    __tablename__ = "alert_log"

    id = Column(Integer, primary_key=True, index=True)
    violation_id = Column(Integer, ForeignKey("violations.id"), nullable=True)
    channel = Column(String)      # "email" | "webhook" | "console"
    status = Column(String)       # "sent" | "failed"
    detail = Column(String, nullable=True)
    timestamp = Column(DateTime, default=dt.datetime.utcnow)
