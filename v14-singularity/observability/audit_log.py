import json
from datetime import datetime


def log(event: dict, decision: dict):
    entry = {"ts": datetime.utcnow().isoformat(), "event": event, "decision": decision}
    with open("audit.log", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")
