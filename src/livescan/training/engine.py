from dataclasses import dataclass

import torch
from torch import nn
from torch.optim import AdamW

from livescan.models.fusion import AdaptiveFusionModel


@dataclass
class TrainState:
    batches_seen: int = 0


class OnlineTrainer:
    def __init__(self, model: AdaptiveFusionModel, lr: float = 3e-4):
        self.model = model
        self.optimizer = AdamW(model.parameters(), lr=lr)
        self.criterion = nn.CrossEntropyLoss()
        self.state = TrainState()

    def train_step(self, node_features: torch.Tensor, adjacency: torch.Tensor, returns_to_go: torch.Tensor, labels: torch.Tensor) -> float:
        self.model.train()
        logits, _ = self.model(node_features, adjacency, returns_to_go)
        loss = self.criterion(logits, labels)
        self.optimizer.zero_grad(set_to_none=True)
        loss.backward()
        self.optimizer.step()
        self.state.batches_seen += 1
        return float(loss.item())


class OfflineTrainer:
    def __init__(self, model: AdaptiveFusionModel, lr: float = 1e-4):
        self.online = OnlineTrainer(model=model, lr=lr)

    def run_epochs(self, dataset: list[dict], epochs: int = 2) -> list[float]:
        losses = []
        for _ in range(epochs):
            for batch in dataset:
                loss = self.online.train_step(
                    node_features=batch["node_features"],
                    adjacency=batch["adjacency"],
                    returns_to_go=batch["returns_to_go"],
                    labels=batch["labels"],
                )
                losses.append(loss)
        return losses
