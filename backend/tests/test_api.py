"""
Basic smoke tests for the PPE Compliance API.
Run with: pytest backend/tests -v
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert "service" in resp.json()


def test_list_cameras_empty_ok():
    resp = client.get("/api/cameras")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)


def test_create_and_delete_camera():
    payload = {"name": "Gate 1", "location": "Site A", "source": "0", "active": True}
    resp = client.post("/api/cameras", json=payload)
    assert resp.status_code == 200
    cam = resp.json()
    assert cam["name"] == "Gate 1"

    del_resp = client.delete(f"/api/cameras/{cam['id']}")
    assert del_resp.status_code == 200


def test_stats_summary_shape():
    resp = client.get("/api/stats/summary")
    assert resp.status_code == 200
    body = resp.json()
    for key in ["total_violations", "violations_today", "compliance_rate_24h",
                "violations_by_type", "violations_by_camera", "trend_last_7_days"]:
        assert key in body
