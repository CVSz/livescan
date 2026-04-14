class World:
    def __init__(self):
        self.memory = []

    def update(self, e):
        self.memory.append(e)
        if len(self.memory) > 2000:
            self.memory.pop(0)
