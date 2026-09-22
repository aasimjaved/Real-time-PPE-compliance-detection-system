"""
Multi-channel alerting: console log (always), email (SMTP), and generic
webhook (Slack/Discord/Teams compatible payload). Any channel that isn't
configured is silently skipped.
"""
import smtplib
import logging
from email.mime.text import MIMEText

import requests

from app.config import settings

logger = logging.getLogger("ppe.alerts")
logging.basicConfig(level=logging.INFO)


def send_console_alert(violation_type: str, camera_name: str, confidence: float) -> None:
    logger.warning(
        "🚨 PPE VIOLATION | camera=%s | type=%s | confidence=%.2f",
        camera_name, violation_type, confidence,
    )


def send_email_alert(violation_type: str, camera_name: str, confidence: float) -> bool:
    if not (settings.SMTP_HOST and settings.SMTP_USER and settings.ALERT_EMAIL_TO):
        return False
    try:
        msg = MIMEText(
            f"PPE violation detected.\n\nCamera: {camera_name}\n"
            f"Violation: {violation_type}\nConfidence: {confidence:.2f}"
        )
        msg["Subject"] = f"[PPE Alert] {violation_type} on {camera_name}"
        msg["From"] = settings.SMTP_USER
        msg["To"] = settings.ALERT_EMAIL_TO

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, [settings.ALERT_EMAIL_TO], msg.as_string())
        return True
    except Exception as exc:  # noqa: BLE001
        logger.error("Email alert failed: %s", exc)
        return False


def send_webhook_alert(violation_type: str, camera_name: str, confidence: float) -> bool:
    if not settings.WEBHOOK_URL:
        return False
    try:
        payload = {
            "text": f"🚨 *PPE Violation*: `{violation_type}` on *{camera_name}* "
                    f"(confidence {confidence:.2f})"
        }
        resp = requests.post(settings.WEBHOOK_URL, json=payload, timeout=5)
        return resp.ok
    except Exception as exc:  # noqa: BLE001
        logger.error("Webhook alert failed: %s", exc)
        return False


def dispatch_alerts(violation_type: str, camera_name: str, confidence: float) -> list[dict]:
    """Fire all configured channels; return a log of what happened for auditing."""
    results = []
    send_console_alert(violation_type, camera_name, confidence)
    results.append({"channel": "console", "status": "sent"})

    if settings.ALERTS_ENABLED:
        if send_email_alert(violation_type, camera_name, confidence):
            results.append({"channel": "email", "status": "sent"})
        if send_webhook_alert(violation_type, camera_name, confidence):
            results.append({"channel": "webhook", "status": "sent"})
    return results
