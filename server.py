import logging
import tomllib

from fastapi import FastAPI

from clients import Database
from util.mount import MountFiles

app = FastAPI()
logger = logging.getLogger("uvicorn")
config = tomllib.load(open("conf.toml", "rb"))
db = Database()


@app.get("/worlds/api/worlds")
async def get_worlds():
    """データベースが持ってるワールドすべてを返す"""
    return db.worlds()


@app.get("/worlds/api/last_updated")
async def get_last_updated():
    """バッチの最終更新時刻"""
    return db.last_updated()


@app.get("/worlds/api/teiban")
async def get_teiban(hr: int, limit: int):
    return db.get_teiban(hr, limit)


@app.get("/worlds/api/hottrend")
async def get_hottrend(hr: int, limit: int):
    return db.get_hottrend(hr, limit)


@app.get("/worlds/api/featured")
async def get_featured(hr: int, limit: int):
    return db.get_featured(hr, limit)


@app.get("/worlds/api/world")
async def get_world(world_id: str, limit: int = 100):
    world_info = db.get_world_info(world_id)
    if not world_info:
        return None
    world_history = db.get_world_history(world_id, limit)
    return {
        "meta": world_info,
        "history": world_history,
    }


app.mount("/worlds/", MountFiles(directory="web/public", html=True), name="static")
