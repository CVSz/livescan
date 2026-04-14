from __future__ import annotations

import torch
import torch.nn as nn

from ml.models.decision_transformer import DecisionTransformer
from ml.models.feature_fusion import FeatureFusion
from ml.models.graph_transformer import GraphTransformer
from ml.models.uncertainty import BayesianHead


class FusionModel(nn.Module):
    """Combines graph, sequence policy, and uncertainty estimation."""

    def __init__(self):
        super().__init__()
        self.graph = GraphTransformer()
        self.feature = FeatureFusion()
        self.policy = DecisionTransformer()
        self.uncertainty = BayesianHead()

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> dict[str, torch.Tensor]:
        g = self.graph(x, adj)
        f = self.feature(x.unsqueeze(0))
        p = self.policy(x.unsqueeze(0))
        mu, std = self.uncertainty(f)

        return {
            "score": g,
            "policy": p,
            "uncertainty": std,
            "value": mu,
        }
