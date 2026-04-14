from __future__ import annotations

from typing import Any

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from ml.models.fusion_model import FusionModel

app = FastAPI(title="v9 inference")
model = FusionModel()
model.eval()


class InferenceRequest(BaseModel):
    seq: list[list[float]] | list[float] = Field(..., min_length=1)


@app.post("/infer")
def infer(payload: InferenceRequest) -> dict[str, Any]:
    x = torch.tensor(payload.seq, dtype=torch.float32)
    if x.dim() == 1:
        x = x.unsqueeze(-1)
    if x.size(0) < 1:
        raise HTTPException(status_code=400, detail="Sequence must be non-empty")
    adj = torch.eye(x.size(0), dtype=torch.float32)

    with torch.no_grad():
        out = model(x, adj)

    return {
        "score": float(out["score"].item() if out["score"].numel() == 1 else out["score"].mean().item()),
        "uncertainty": float(out["uncertainty"].mean().item()),
        "value": float(out["value"].mean().item()),
        "policy": float(out["policy"].mean().item()),
    }
