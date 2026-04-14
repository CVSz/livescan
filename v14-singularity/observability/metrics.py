from prometheus_client import Counter

decisions_total = Counter("decisions_total", "Total decisions")


def record():
    decisions_total.inc()
