from fastapi import FastAPI

from core.orchestrator import run

app = FastAPI()


@app.post("/event")
def event(e: dict):
    return run(e)
