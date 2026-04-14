import torch


def fused_linear(x: torch.Tensor, weight: torch.Tensor, bias: torch.Tensor | None = None) -> torch.Tensor:
    out = x @ weight.T
    if bias is not None:
        out = out + bias
    return out
