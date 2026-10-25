"""Tests for Self-Healing Code logic and API behavior."""
from fastapi.testclient import TestClient

from app.logic import LogicError, run
from app.main import app

SAMPLE = {'code': 'def load(path):\n'
         '    try:\n'
         '        return open(path).read()\n'
         '    except:\n'
         '        return None\n'
         '\n'
         'if load("x") == None:\n'
         '    print("missing")'}


def test_sample_run():
    res = run(SAMPLE)
    assert res["summary"]
    assert isinstance(res["result"], dict)
    assert res['result']['metrics']['issues'] >= 1
    assert res['result']['patches']


def test_empty_payload_is_rejected():
    try:
        run({})
    except LogicError:
        return
    raise AssertionError("empty payload should raise LogicError")


def test_health_and_meta():
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    meta = client.get("/api/meta")
    assert meta.status_code == 200
    assert meta.json()["agent"] == "plotxyz-self-healing-code-agent"


def test_run_endpoint_and_history():
    client = TestClient(app)
    response = client.post("/api/run", json={"payload": SAMPLE})
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["summary"]
    assert body["task_id"] is not None
    history = client.get("/api/history?limit=5")
    assert history.status_code == 200
    assert len(history.json()["items"]) >= 1


def test_invalid_payload_returns_422():
    client = TestClient(app)
    response = client.post("/api/run", json={"payload": {}})
    assert response.status_code == 422


def test_payload_limit_returns_413():
    client = TestClient(app)
    response = client.post("/api/run", json={"payload": {"blob": "x" * 200001}})
    assert response.status_code == 413
