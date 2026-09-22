"""
Central configuration for the PPE Compliance Detection backend.
All values are overridable via environment variables (see .env.example).
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    # --- App ---
    APP_NAME: str = "PPE Compliance Detection System"
    ENV: str = os.getenv("ENV", "development")

    # --- Database ---
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR}/ppe_compliance.db")

    # --- Model ---
    # Point this at your trained PPE weights (see backend/train/train_model.py).
    # Falls back to a stock YOLOv8n (COCO) model for person-only detection so the
    # app runs out of the box before you train a custom model.
    MODEL_PATH: str = os.getenv("MODEL_PATH", "yolov8n.pt")
    CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.45"))
    IOU_THRESHOLD: float = float(os.getenv("IOU_THRESHOLD", "0.45"))

    # Class names for a model trained on a standard PPE dataset
    # (e.g. Roboflow "Construction Site Safety" PPE dataset).
    PPE_CLASSES = [
        "Hardhat", "Mask", "NO-Hardhat", "NO-Mask", "NO-Safety Vest",
        "Person", "Safety Cone", "Safety Vest", "machinery", "vehicle",
    ]
    VIOLATION_CLASSES = {"NO-Hardhat", "NO-Mask", "NO-Safety Vest"}

    # How many consecutive frames a violation must appear in before it's logged
    # (debounces flicker / momentary misdetections).
    VIOLATION_FRAME_THRESHOLD: int = int(os.getenv("VIOLATION_FRAME_THRESHOLD", "5"))
    # Minimum seconds between two logged violations of the same type on the same camera
    VIOLATION_COOLDOWN_SECONDS: int = int(os.getenv("VIOLATION_COOLDOWN_SECONDS", "30"))

    # --- Alerts ---
    ALERTS_ENABLED: bool = os.getenv("ALERTS_ENABLED", "true").lower() == "true"
    SMTP_HOST: str = os.getenv("SMTP_HOST", "")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    ALERT_EMAIL_TO: str = os.getenv("ALERT_EMAIL_TO", "")
    WEBHOOK_URL: str = os.getenv("WEBHOOK_URL", "")  # e.g. Slack/Discord incoming webhook

    # --- Storage ---
    VIOLATION_SNAPSHOTS_DIR: Path = BASE_DIR / "snapshots"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")


settings = Settings()
settings.VIOLATION_SNAPSHOTS_DIR.mkdir(parents=True, exist_ok=True)
