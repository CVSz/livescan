from __future__ import annotations


class CEP:
    def __init__(self):
        self.buffer: list[dict] = []

    def process(self, event: dict) -> dict:
        self.buffer.append(event)
        if len(self.buffer) > 5:
            self.buffer.pop(0)

        if len(self.buffer) >= 3:
            m = [e["multiplier"] for e in self.buffer[-3:]]
            if m[0] < m[1] < m[2]:
                event["pattern"] = "CHAIN"
        return event
