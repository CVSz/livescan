import torch
from torch import nn


class GraphAttentionBlock(nn.Module):
    def __init__(self, dim: int, heads: int):
        super().__init__()
        self.attn = nn.MultiheadAttention(embed_dim=dim, num_heads=heads, batch_first=True)
        self.ffn = nn.Sequential(nn.Linear(dim, dim * 2), nn.GELU(), nn.Linear(dim * 2, dim))
        self.norm1 = nn.LayerNorm(dim)
        self.norm2 = nn.LayerNorm(dim)

    def forward(self, x: torch.Tensor, adjacency: torch.Tensor) -> torch.Tensor:
        mask = adjacency <= 0
        attn_out, _ = self.attn(x, x, x, attn_mask=mask[: x.shape[1], : x.shape[1]])
        x = self.norm1(x + attn_out)
        return self.norm2(x + self.ffn(x))


class GNNGraphTransformer(nn.Module):
    def __init__(self, in_dim: int, model_dim: int, heads: int, layers: int):
        super().__init__()
        self.in_proj = nn.Linear(in_dim, model_dim)
        self.layers = nn.ModuleList([GraphAttentionBlock(model_dim, heads) for _ in range(layers)])
        self.out_norm = nn.LayerNorm(model_dim)

    def forward(self, node_features: torch.Tensor, adjacency: torch.Tensor) -> torch.Tensor:
        x = self.in_proj(node_features).unsqueeze(0)
        for layer in self.layers:
            x = layer(x, adjacency)
        x = self.out_norm(x)
        return x.mean(dim=1)
