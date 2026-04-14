from prometheus_client import Counter

decisions = Counter("ai_decisions_total", "Total sovereign decisions")


def record() -> None:
    decisions.inc()
