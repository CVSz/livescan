from fastapi import FastAPI

from core.orchestrator import run

app = FastAPI()


@app.post("/simulate")
def simulate(e: dict):
    return run(e)
