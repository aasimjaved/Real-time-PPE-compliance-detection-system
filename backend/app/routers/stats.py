import datetime as dt
from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db
from app import models
from app.schemas import StatsSummary

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/summary", response_model=StatsSummary)
def summary(db: Session = Depends(get_db)):
    now = dt.datetime.utcnow()
    today_start = dt.datetime(now.year, now.month, now.day)
    last_24h = now - dt.timedelta(hours=24)
    last_7d = now - dt.timedelta(days=7)

    total = db.query(func.count(models.Violation.id)).scalar() or 0
    today = db.query(func.count(models.Violation.id)).filter(
        models.Violation.timestamp >= today_start
    ).scalar() or 0

    recent = db.query(models.Violation).filter(models.Violation.timestamp >= last_24h).all()
    by_type = Counter(v.violation_type for v in recent)
    by_camera = Counter(str(v.camera_id) for v in recent)

    # crude "compliance rate" proxy: fewer violations in the window = higher score,
    # capped at 0-100 for a simple headline KPI on the dashboard.
    compliance_rate = max(0.0, 100.0 - min(len(recent), 100))

    trend = []
    week_violations = db.query(models.Violation).filter(models.Violation.timestamp >= last_7d).all()
    by_day = Counter(v.timestamp.date().isoformat() for v in week_violations)
    for i in range(6, -1, -1):
        day = (now - dt.timedelta(days=i)).date().isoformat()
        trend.append({"date": day, "violations": by_day.get(day, 0)})

    return StatsSummary(
        total_violations=total,
        violations_today=today,
        compliance_rate_24h=compliance_rate,
        violations_by_type=dict(by_type),
        violations_by_camera=dict(by_camera),
        trend_last_7_days=trend,
    )
