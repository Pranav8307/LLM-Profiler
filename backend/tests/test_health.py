import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_all_ok():
    with patch("app.services.health.check_db_connection", return_value=True), \
         patch("app.services.health.check_redis_connection", return_value=True):
        resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["services"]["database"]["status"] == "ok"
    assert data["services"]["redis"]["status"] == "ok"


def test_health_db_down():
    with patch("app.services.health.check_db_connection", return_value=False), \
         patch("app.services.health.check_redis_connection", return_value=True):
        resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "degraded"
    assert data["services"]["database"]["status"] == "down"


def test_health_redis_down():
    with patch("app.services.health.check_db_connection", return_value=True), \
         patch("app.services.health.check_redis_connection", return_value=False):
        resp = client.get("/api/v1/health")
    data = resp.json()
    assert data["status"] == "degraded"
    assert data["services"]["redis"]["status"] == "down"