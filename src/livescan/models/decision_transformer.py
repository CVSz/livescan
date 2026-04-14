import torch
from torch import nn


class DecisionTransformer(nn.Module):
    def __init__(self, state_dim: int, action_dim: int, model_dim: int, heads: int, layers: int):
        super().__init__()
        self.state_embed = nn.Linear(state_dim, model_dim)
        self.rtg_embed = nn.Linear(1, model_dim)
        self.action_head = nn.Linear(model_dim, action_dim)
        enc_layer = nn.TransformerEncoderLayer(d_model=model_dim, nhead=heads, batch_first=True)
        self.encoder = nn.TransformerEncoder(enc_layer, num_layers=layers)

    def forward(self, states: torch.Tensor, returns_to_go: torch.Tensor) -> torch.Tensor:
        state_toks = self.state_embed(states)
        rtg_toks = self.rtg_embed(returns_to_go.unsqueeze(-1))
        seq = state_toks + rtg_toks
        hidden = self.encoder(seq)
        return self.action_head(hidden[:, -1, :])
