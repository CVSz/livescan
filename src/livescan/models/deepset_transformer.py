import torch
from torch import nn


class DeepSetTransformer(nn.Module):
    def __init__(self, input_dim: int, model_dim: int, heads: int):
        super().__init__()
        self.phi = nn.Sequential(
            nn.Linear(input_dim, model_dim),
            nn.ReLU(),
            nn.Linear(model_dim, model_dim),
        )
        encoder_layer = nn.TransformerEncoderLayer(d_model=model_dim, nhead=heads, batch_first=True)
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=2)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.phi(x)
        x = self.encoder(x)
        return x.mean(dim=1)
