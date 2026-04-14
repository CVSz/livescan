from __future__ import annotations

import torch
import torch.nn as nn


class BayesianHead(nn.Module):
    """Bayesian-style uncertainty head returning mean and std."""

    def __init__(self, hidden_dim: int = 64):
        super().__init__()
        self.mu = nn.Linear(hidden_dim, 1)
        self.log_var = nn.Linear(hidden_dim, 1)

    def forward(self, fused: torch.Tensor) -> tuple[torch.Tensor, torch.Tensor]:
        mu = self.mu(fused).squeeze(-1)
        log_var = self.log_var(fused).squeeze(-1)
        std = torch.exp(0.5 * torch.clamp(log_var, min=-10.0, max=10.0))
        return mu, std
