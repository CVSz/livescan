from __future__ import annotations

import torch
import torch.nn as nn


class DecisionTransformer(nn.Module):
    """Sequence policy head for online decision simulation."""

    def __init__(self, input_dim: int = 4, d_model: int = 64, nhead: int = 4):
        super().__init__()
        self.in_proj = nn.Linear(input_dim, d_model)
        layer = nn.TransformerEncoderLayer(d_model=d_model, nhead=nhead, batch_first=True)
        self.encoder = nn.TransformerEncoder(layer, num_layers=2)
        self.policy_head = nn.Linear(d_model, 1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.dim() == 2:
            x = x.unsqueeze(0)
        if x.size(-1) == 1:
            x = x.repeat(1, 1, 4)
        h = self.encoder(self.in_proj(x))
        logits = self.policy_head(h[:, -1, :])
        return torch.sigmoid(logits).squeeze(-1)
