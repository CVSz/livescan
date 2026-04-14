import torch
from torch import nn


class MaskedNodePretrainer(nn.Module):
    def __init__(self, backbone: nn.Module, feature_dim: int):
        super().__init__()
        self.backbone = backbone
        self.reconstruct = nn.Linear(feature_dim, feature_dim)
        self.loss_fn = nn.MSELoss()

    def step(self, node_features: torch.Tensor, adjacency: torch.Tensor, returns_to_go: torch.Tensor):
        mask = torch.rand_like(node_features) < 0.15
        masked_input = node_features.clone()
        masked_input[mask] = 0.0
        pred, _ = self.backbone(masked_input, adjacency, returns_to_go)
        target = node_features.mean(dim=0, keepdim=True)
        pred = self.reconstruct(pred)
        loss = self.loss_fn(pred, target)
        return loss
