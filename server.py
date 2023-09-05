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
def get_worlds():
    """データベースが持ってるワールドすべてを返す"""
    return db.worlds()


@app.get("/worlds/api/last_updated")
def get_last_updated():
    """バッチの最終更新時刻"""
    return db.last_updated()


@app.get("/worlds/api/teiban")
def get_teiban(limit: int, new: bool = False):
    return db.get_teiban(limit, new)


@app.get("/worlds/api/trend")
def get_trend(hr: int, limit: int, new: bool = False):
    return db.get_trend(hr, limit, new)


@app.get("/worlds/api/hottrend")
def get_hottrend(hr: int, limit: int, new: bool = False):
    return db.get_hottrend(hr, limit, new)


@app.get("/worlds/api/featured")
def get_featured(hr: int, limit: int, new: bool = False):
    return db.get_featured(hr, limit, new)


@app.get("/worlds/api/world")
def get_world(world_id: str, limit: int = 100):
    world_info = db.get_world_info(world_id)
    if not world_info:
        return None
    world_history = db.get_world_history(world_id, limit)
    return {
        "meta": world_info,
        "history": world_history,
    }


app.mount("/worlds/", MountFiles(directory="web/public", html=True), name="static")
