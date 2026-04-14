from typing import List
from pydantic import BaseModel, Field


class Event(BaseModel):
    ts: int
    src: int
    dst: int
    weight: float = 1.0
    features: List[float] = Field(default_factory=list)
    reward: float = 0.0
    action: int = 0


class PredictRequest(BaseModel):
    events: List[Event]


class PredictResponse(BaseModel):
    logits: List[float]
    action: int
    uncertainty: float
    route: str


class TrainStepResponse(BaseModel):
    loss: float
    batches_seen: int
