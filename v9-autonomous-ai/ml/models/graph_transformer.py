from __future__ import annotations

import torch
import torch.nn as nn


class GraphTransformer(nn.Module):
    """Minimal graph-aware encoder using adjacency weighted aggregation."""

    def __init__(self, input_dim: int = 4, hidden_dim: int = 64):
        super().__init__()
        self.node_proj = nn.Linear(input_dim, hidden_dim)
        self.out_proj = nn.Linear(hidden_dim, 1)
        self.norm = nn.LayerNorm(hidden_dim)

    def forward(self, x: torch.Tensor, adj: torch.Tensor) -> torch.Tensor:
        if x.dim() == 1:
            x = x.unsqueeze(-1)
        if x.dim() == 2 and x.size(-1) == 1:
            x = x.repeat(1, 4)

        h = self.node_proj(x)
        h = torch.matmul(adj, h)
        h = self.norm(torch.relu(h))
        graph_state = h.mean(dim=0)
        return self.out_proj(graph_state).squeeze(-1)
