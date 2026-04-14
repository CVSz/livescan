class World:
    def __init__(self):
        self.memory = []

    def update(self, event):
        self.memory.append(event)
        if len(self.memory) > 1000:
            self.memory.pop(0)

    def state(self):
        return self.memory[-1] if self.memory else {}
