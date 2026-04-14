import torch
import torch.nn as nn


class MetaRL(nn.Module):
    """Lightweight meta-RL block that adapts policy logits from event state."""

    def __init__(self, in_dim: int = 4, hidden_dim: int = 64, action_dim: int = 4) -> None:
        super().__init__()
        self.encoder = nn.Linear(in_dim, hidden_dim)
        self.policy = nn.Linear(hidden_dim, action_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        h = torch.relu(self.encoder(x))
        return torch.softmax(self.policy(h), dim=-1)

    def adapt(self, loss: torch.Tensor) -> None:
        loss.backward()
