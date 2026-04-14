import numpy as np


class CausalEngine:
    """Simple causal checks for treatment effects and spurious signals."""

    def estimate_effect(self, x: np.ndarray, y: np.ndarray) -> float:
        x = np.asarray(x)
        y = np.asarray(y, dtype=float)
        if np.sum(x == 1) == 0 or np.sum(x == 0) == 0:
            return 0.0
        return float(np.mean(y[x == 1]) - np.mean(y[x == 0]))

    def detect_spurious(self, corr: float, effect: float, threshold: float = 0.5) -> bool:
        return abs(corr - effect) > threshold
