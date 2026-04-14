import random


class NAS:
    def sample(self):
        return {"hidden": random.choice([32, 64, 128]), "layers": random.choice([1, 2, 3])}
