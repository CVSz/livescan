from fastapi import FastAPI

from core.orchestrator import run

app = FastAPI()


@app.get("/")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/event")
def event(e: dict):
    return run(e)
