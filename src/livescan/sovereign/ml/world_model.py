from __future__ import annotations

import numpy as np


class WorldModel:
    def __init__(self, max_memory: int = 1000) -> None:
        self.max_memory = max_memory
        self.memory: list[dict[str, float]] = []

    def update(self, event: dict[str, float]) -> None:
        self.memory.append(event)
        if len(self.memory) > self.max_memory:
            self.memory.pop(0)

    def embed(self) -> np.ndarray:
        if not self.memory:
            return np.zeros(4)
        vectors = np.array(
            [[float(item.get("reward", 0.0)), float(item.get("uncertainty", 0.0)), float(item.get("signal", 0.0)), float(item.get("load", 0.0))] for item in self.memory],
            dtype=float,
        )
        return np.mean(vectors, axis=0)
