from __future__ import annotations

import torch
import torch.nn as nn


class FeatureFusion(nn.Module):
    """Fuses temporal and static features into a compact representation."""

    def __init__(self, input_dim: int = 4, hidden_dim: int = 64):
        super().__init__()
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 2:
            x = x.unsqueeze(0)
        if x.size(-1) == 1:
            x = x.repeat(1, 1, 4)
        encoded = self.encoder(x)
        return encoded.mean(dim=1)
