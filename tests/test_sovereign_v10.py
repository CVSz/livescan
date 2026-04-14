from fastapi.testclient import TestClient

from livescan.api.main import app
from livescan.sovereign.ml.causal import CausalEngine
from livescan.sovereign.ml.world_model import WorldModel


def test_v10_event_endpoint():
    client = TestClient(app)
    res = client.post("/v10/event", json={"reward": 0.9, "uncertainty": 0.2, "plan": "apply_policy"})
    assert res.status_code == 200
    body = res.json()
    assert body["Auditor"]["risk"] == "LOW"
    assert "Planner" in body


def test_world_model_embed_shape():
    model = WorldModel()
    model.update({"reward": 1.0, "uncertainty": 0.2, "signal": 0.5, "load": 0.7})
    assert model.embed().shape == (4,)


def test_causal_engine_effect():
    engine = CausalEngine()
    effect = engine.estimate_effect(x=[0, 1, 1, 0], y=[1.0, 2.0, 2.5, 0.5])
    assert effect > 1.0
