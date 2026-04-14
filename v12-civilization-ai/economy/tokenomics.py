class Tokenomics:
    def __init__(self):
        self.supply = 1_000_000

    def burn(self, amount):
        self.supply -= amount

    def mint(self, amount):
        self.supply += amount
