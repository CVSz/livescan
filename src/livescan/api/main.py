from contextlib import asynccontextmanager

import torch
from fastapi import FastAPI, HTTPException
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
from starlette.responses import Response

from livescan.api.schemas import PredictRequest, PredictResponse, TrainStepResponse
from livescan.models.fusion import AdaptiveFusionModel
from livescan.models.temporal_graph import TemporalGraphBuilder
from livescan.models.uncertainty import mc_dropout_predict
from livescan.sovereign.core.orchestrator import loop as sovereign_loop
from livescan.sovereign.observability.metrics import record as record_sovereign_decision
from livescan.training.engine import OnlineTrainer
from livescan.utils.config import CONFIG
from livescan.utils.logging import build_logger

logger = build_logger("livescan-api")
REQ_COUNT = Counter("livescan_requests_total", "Total prediction requests")
LATENCY = Histogram("livescan_request_latency_seconds", "Prediction latency")
TRAIN_COUNT = Counter("livescan_train_steps_total", "Total online train steps")


def build_runtime():
    model = AdaptiveFusionModel(
        in_dim=16,
        action_dim=CONFIG.action_dim,
        model_dim=CONFIG.model_dim,
        heads=CONFIG.num_heads,
        layers=CONFIG.num_layers,
    )
    graph_builder = TemporalGraphBuilder(max_nodes=CONFIG.max_nodes, feature_dim=16)
    trainer = OnlineTrainer(model, lr=CONFIG.learning_rate)
    return model, graph_builder, trainer


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("startup")
    yield
    logger.info("shutdown")


app = FastAPI(title="LiveScan Inference API", lifespan=lifespan)
MODEL, GRAPH, TRAINER = build_runtime()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.post("/predict", response_model=PredictResponse)
def predict(payload: PredictRequest):
    REQ_COUNT.inc()
    with LATENCY.time():
        events = [e.model_dump() for e in payload.events]
        if not events:
            raise HTTPException(status_code=400, detail="events must not be empty")
        batch = GRAPH.update(events)
        returns = batch.rewards.cumsum(dim=0)[-1:].float()
        mean_logits, uncertainty, route = mc_dropout_predict(
            MODEL,
            {
                "node_features": batch.node_features,
                "adjacency": batch.adjacency,
                "returns_to_go": returns,
            },
            samples=CONFIG.mc_samples,
        )
        action = int(torch.argmax(mean_logits, dim=-1).item())
        return PredictResponse(
            logits=mean_logits.squeeze(0).tolist(),
            action=action,
            uncertainty=uncertainty,
            route=str(route),
        )


@app.post("/train/step", response_model=TrainStepResponse)
def train_step(payload: PredictRequest):
    events = [e.model_dump() for e in payload.events]
    if not events:
        raise HTTPException(status_code=400, detail="events must not be empty")
    batch = GRAPH.update(events)
    returns = batch.rewards.cumsum(dim=0)[-1:].float()
    label = torch.tensor([batch.actions[-1].item() % CONFIG.action_dim], dtype=torch.long)
    loss = TRAINER.train_step(batch.node_features, batch.adjacency, returns, label)
    TRAIN_COUNT.inc()
    return TrainStepResponse(loss=loss, batches_seen=TRAINER.state.batches_seen)


@app.post("/v10/event")
def process_sovereign_event(event: dict):
    decision = sovereign_loop(event)
    record_sovereign_decision()
    return decision
