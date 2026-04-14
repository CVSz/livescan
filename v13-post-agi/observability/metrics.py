from prometheus_client import Counter

metrics = Counter("events_total", "Total events")
