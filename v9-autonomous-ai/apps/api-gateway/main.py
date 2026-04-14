from __future__ import annotations

import os
import time
from collections import defaultdict, deque

import jwt
from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="v9 api gateway")
SECRET = os.getenv("JWT_SECRET", "CHANGE_ME")
RATE = int(os.getenv("RATE_LIMIT_PER_MIN", "120"))
WINDOW_SECONDS = 60
requests_by_ip: dict[str, deque[float]] = defaultdict(deque)


@app.middleware("http")
async def auth(request: Request, call_next):
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    window = requests_by_ip[ip]

    while window and now - window[0] > WINDOW_SECONDS:
        window.popleft()
    if len(window) >= RATE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")

    try:
        jwt.decode(token, SECRET, algorithms=["HS256"])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=403, detail="Invalid token") from exc

    window.append(now)
    return await call_next(request)
