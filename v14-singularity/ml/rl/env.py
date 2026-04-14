import numpy as np


class Env:
    def reset(self):
        self.balance = 1000.0
        return self._state()

    def step(self, a: int):
        bet = [1, 2, 5, 10][a]
        win = bet * (1 + np.random.rand()) if np.random.rand() < 0.3 else 0.0
        r = win - bet
        self.balance += r
        done = self.balance <= 0
        return self._state(), r, done

    def _state(self):
        return np.random.rand(4)
