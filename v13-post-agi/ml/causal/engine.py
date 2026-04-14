import numpy as np


class Causal:
    def effect(self, x, y):
        return np.mean(y[x == 1]) - np.mean(y[x == 0])
