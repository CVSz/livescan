class CEP:
    def __init__(self):
        self.buf = []

    def process(self, event):
        self.buf.append(event)
        if len(self.buf) > 3:
            self.buf.pop(0)

        if len(self.buf) == 3:
            if self.buf[0]["mult"] < self.buf[1]["mult"] < self.buf[2]["mult"]:
                event["pattern"] = "CHAIN"
        return event
