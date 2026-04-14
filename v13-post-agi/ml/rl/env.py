import numpy as np


class Env:
    def reset(self):
        self.balance = 1000
        return self._state()

    def step(self, a):
        bet = [1, 2, 5, 10][a]
        win = bet * np.random.rand() * 2 if np.random.rand() < 0.3 else 0
        r = win - bet
        self.balance += r
        return self._state(), r, self.balance <= 0

    def _state(self):
        return np.random.rand(4)
