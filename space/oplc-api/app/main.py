# app/main.py
from __future__ import annotations
import os, random
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

USER_AGENT = os.getenv("USER_AGENT", "OPLC/1.0 (+https://github.com/your-org/oplc)")
BACKEND_MODE = os.getenv("BACKEND_MODE", "proxy").lower()
ENABLE_PADDING = os.getenv("PADDING", "true").lower() == "true"
HIBP_RANGE_URL = "https://api.pwnedpasswords.com/range/{}"
HEX = "0123456789ABCDEF"

def validate_prefix(prefix: str) -> None:
    if len(prefix) != 5 or any(c not in HEX for c in prefix):
        raise ValueError("prefix must be 5 hex chars (SHA-1 uppercased)")

app = FastAPI(title="Open Password Leak Check (OPLC)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=False,
    allow_methods=["GET"], allow_headers=["*"],
)

@app.get("/healthz", response_class=PlainTextResponse)
async def healthz() -> str:
    return "ok"

@app.get("/range/{prefix}", response_class=PlainTextResponse)
async def range_lookup(prefix: str):
    prefix = prefix.strip().upper()
    try:
        validate_prefix(prefix)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if BACKEND_MODE == "proxy":
        async with httpx.AsyncClient(
            timeout=30.0,
            headers={"User-Agent": USER_AGENT, "Add-Padding": "true" if ENABLE_PADDING else "false"},
        ) as client:
            r = await client.get(HIBP_RANGE_URL.format(prefix))
            if r.status_code != 200:
                raise HTTPException(status_code=502, detail=f"Upstream error: {r.status_code}")
            return PlainTextResponse(r.text, headers={"Cache-Control": "max-age=86400, public"})

    elif BACKEND_MODE == "hf":
        # Import here so proxy mode never imports storage (avoids cache dir on startup)
        from .storage import get_suffixes_from_hf
        suffixes = await get_suffixes_from_hf(prefix)
        if ENABLE_PADDING:
            suffixes = add_padding(suffixes)
        suffixes.sort()
        return PlainTextResponse("\n".join(suffixes), headers={"Cache-Control": "max-age=86400, public"})

    raise HTTPException(status_code=500, detail="Unsupported BACKEND_MODE")

def add_padding(suffixes: list[str]) -> list[str]:
    # why: reduce info leakage via response size
    n = len(suffixes); target = 800; extra = random.randint(0, 200)
    needed = max(0, target - n) + extra
    if needed == 0: return suffixes
    padded = list(suffixes)
    for _ in range(needed):
        dummy = f"{random.getrandbits(4*35):035x}".upper()
        padded.append(f"{dummy}:0")
    return padded
