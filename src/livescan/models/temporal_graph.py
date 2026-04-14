from collections import deque
from dataclasses import dataclass
from typing import Deque, Iterable

import networkx as nx
import torch


@dataclass
class GraphBatch:
    node_features: torch.Tensor
    adjacency: torch.Tensor
    rewards: torch.Tensor
    actions: torch.Tensor


class TemporalGraphBuilder:
    def __init__(self, max_nodes: int = 128, feature_dim: int = 16, window_size: int = 256):
        self.max_nodes = max_nodes
        self.feature_dim = feature_dim
        self.window: Deque[dict] = deque(maxlen=window_size)

    def update(self, events: Iterable[dict]) -> GraphBatch:
        for event in events:
            self.window.append(event)

        g = nx.DiGraph()
        for event in self.window:
            src = int(event["src"])
            dst = int(event["dst"])
            g.add_edge(src, dst, weight=float(event.get("weight", 1.0)))

        nodes = sorted(g.nodes())[: self.max_nodes]
        node_index = {n: i for i, n in enumerate(nodes)}
        node_features = torch.zeros((self.max_nodes, self.feature_dim), dtype=torch.float32)
        adjacency = torch.zeros((self.max_nodes, self.max_nodes), dtype=torch.float32)

        for event in list(self.window)[-self.max_nodes :]:
            src = event["src"]
            dst = event["dst"]
            if src in node_index and dst in node_index:
                i, j = node_index[src], node_index[dst]
                adjacency[i, j] = float(event.get("weight", 1.0))
                feats = event.get("features", [])[: self.feature_dim]
                if feats:
                    node_features[i, : len(feats)] = torch.tensor(feats, dtype=torch.float32)

        rewards = torch.tensor([e.get("reward", 0.0) for e in list(self.window)[-self.max_nodes :]], dtype=torch.float32)
        actions = torch.tensor([e.get("action", 0) for e in list(self.window)[-self.max_nodes :]], dtype=torch.long)
        if rewards.numel() == 0:
            rewards = torch.zeros(1, dtype=torch.float32)
            actions = torch.zeros(1, dtype=torch.long)
        return GraphBatch(node_features=node_features, adjacency=adjacency, rewards=rewards, actions=actions)
