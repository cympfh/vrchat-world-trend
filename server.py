import logging
from typing import Optional

from fastapi import FastAPI

from util.mount import MountFiles

app = FastAPI()
logger = logging.getLogger("uvicorn")


@app.get("/api/greeting")
def greeting(name: Optional[str] = None):
    """Greeting you"""
    if name:
        return {"msg": f"Hello {name}!"}
    return {"msg": "Hi!"}


app.mount("/", MountFiles(directory="web/public", html=True), name="static")
