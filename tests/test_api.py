from fastapi.testclient import TestClient

from livescan.api.main import app


def test_healthz():
    client = TestClient(app)
    res = client.get("/healthz")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"


def test_predict_and_train_step():
    client = TestClient(app)
    payload = {
        "events": [
            {"ts": 1, "src": 1, "dst": 2, "weight": 1.0, "features": [0.1] * 16, "reward": 0.5, "action": 1},
            {"ts": 2, "src": 2, "dst": 3, "weight": 2.0, "features": [0.2] * 16, "reward": 1.0, "action": 2},
        ]
    }
    pred = client.post("/predict", json=payload)
    assert pred.status_code == 200
    body = pred.json()
    assert "action" in body
    step = client.post("/train/step", json=payload)
    assert step.status_code == 200
    assert step.json()["batches_seen"] >= 1
