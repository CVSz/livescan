from __future__ import annotations

import numpy as np


class WorldModel:
    """
    Represents global state for agents, economy, and environment snapshots.
    """

    def __init__(self):
        self.state = []
        self.resources = {"energy": 1000, "capital": 1000}

    def update(self, event: dict):
        self.state.append(event)
        if len(self.state) > 5000:
            self.state.pop(0)

    def aggregate(self):
        if not self.state:
            return np.zeros(4)
        return np.mean([list(event.values())[:4] for event in self.state], axis=0)

    def allocate(self, cost: float):
        if self.resources["capital"] >= cost:
            self.resources["capital"] -= cost
            return True
        return False
