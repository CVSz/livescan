from __future__ import annotations

import torch
import torch.optim as optim

from ml.models.fusion_model import FusionModel


class OnlineTrainer:
    def __init__(self, lr: float = 1e-4):
        self.model = FusionModel()
        self.opt = optim.Adam(self.model.parameters(), lr=lr)

    def train_batch(self, x: torch.Tensor, adj: torch.Tensor) -> float:
        self.model.train()
        out = self.model(x, adj)

        loss = (
            out["score"].mean()
            + out["uncertainty"].mean()
            - out["policy"].mean()
            + 0.1 * out["value"].pow(2).mean()
        )

        self.opt.zero_grad()
        loss.backward()
        self.opt.step()

        return float(loss.item())
