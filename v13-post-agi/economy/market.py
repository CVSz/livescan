class Market:
    def __init__(self):
        self.price = 1.0

    def update(self, d, s):
        self.price += (d - s) * 0.01
        return self.price
