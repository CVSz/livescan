import torch
import torch.nn as nn


class Fusion(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(4, 64)
        self.policy = nn.Linear(64, 4)

    def forward(self, x):
        h = torch.relu(self.fc(x))
        return torch.softmax(self.policy(h), dim=-1)
