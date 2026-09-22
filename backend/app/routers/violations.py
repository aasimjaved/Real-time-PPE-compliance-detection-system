from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/api/violations", tags=["violations"])


@router.get("", response_model=List[schemas.ViolationOut])
def list_violations(
    db: Session = Depends(get_db),
    camera_id: Optional[int] = None,
    violation_type: Optional[str] = None,
    resolved: Optional[bool] = None,
    limit: int = Query(100, le=1000),
):
    q = db.query(models.Violation)
    if camera_id is not None:
        q = q.filter(models.Violation.camera_id == camera_id)
    if violation_type is not None:
        q = q.filter(models.Violation.violation_type == violation_type)
    if resolved is not None:
        q = q.filter(models.Violation.resolved == resolved)
    return q.order_by(models.Violation.timestamp.desc()).limit(limit).all()


@router.patch("/{violation_id}/resolve", response_model=schemas.ViolationOut)
def resolve_violation(violation_id: int, db: Session = Depends(get_db)):
    v = db.query(models.Violation).filter(models.Violation.id == violation_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Violation not found")
    v.resolved = True
    db.commit()
    db.refresh(v)
    return v
