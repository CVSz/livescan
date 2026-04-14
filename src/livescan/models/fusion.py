import torch
from torch import nn

from livescan.models.decision_transformer import DecisionTransformer
from livescan.models.deepset_transformer import DeepSetTransformer
from livescan.models.gnn_transformer import GNNGraphTransformer


class AdaptiveFusionModel(nn.Module):
    def __init__(self, in_dim: int, action_dim: int, model_dim: int, heads: int, layers: int):
        super().__init__()
        self.gnn = GNNGraphTransformer(in_dim, model_dim, heads, layers)
        self.set_model = DeepSetTransformer(in_dim, model_dim, heads)
        self.decision = DecisionTransformer(model_dim, action_dim, model_dim, heads, layers)
        self.decision_proj = nn.Linear(action_dim, model_dim)
        self.router = nn.Sequential(
            nn.Linear(model_dim * 2, model_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(model_dim, 3),
        )
        self.head = nn.Linear(model_dim * 3, action_dim)

    def forward(self, node_features: torch.Tensor, adjacency: torch.Tensor, returns_to_go: torch.Tensor):
        graph_repr = self.gnn(node_features, adjacency)
        set_repr = self.set_model(node_features.unsqueeze(0))
        decision_logits = self.decision(graph_repr.unsqueeze(1), returns_to_go.unsqueeze(0))
        route_logits = self.router(torch.cat([graph_repr, set_repr], dim=-1))
        route = torch.argmax(route_logits, dim=-1)
        decision_repr = self.decision_proj(decision_logits)
        fused = torch.cat([graph_repr, set_repr, decision_repr], dim=-1)
        return self.head(fused), route.item()
