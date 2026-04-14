class CEP:
    def __init__(self):
        self.buf = []

    def process(self, e):
        self.buf.append(e)
        if len(self.buf) > 3:
            self.buf.pop(0)

        if len(self.buf) == 3:
            m = [x.get("mult", 1) for x in self.buf]
            if m[0] < m[1] < m[2]:
                e["pattern"] = "CHAIN"
        return e
