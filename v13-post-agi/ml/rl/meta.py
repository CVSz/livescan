import torch
import torch.nn as nn


class MetaRL(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(4, 64)
        self.out = nn.Linear(64, 4)

    def forward(self, x):
        return torch.softmax(self.out(torch.relu(self.fc(x))), dim=-1)
