class Market:
    def __init__(self):
        self.price = 1.0

    def update(self, demand, supply):
        delta = (demand - supply) * 0.01
        self.price = max(0.1, self.price + delta)
        return self.price
