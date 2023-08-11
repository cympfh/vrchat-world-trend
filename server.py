import logging
import tomllib

from fastapi import FastAPI

from clients import Database
from util.mount import MountFiles

app = FastAPI()
logger = logging.getLogger("uvicorn")
config = tomllib.load(open("conf.toml", "rb"))
db = Database()


@app.get("/api/worlds")
def get_worlds():
    """データベースが持ってるワールドすべてを返す"""
    return db.worlds()


@app.get("/api/last_updated")
def get_last_updated():
    """バッチの最終更新時刻"""
    return db.last_updated()


@app.get("/api/teiban")
def get_teiban(limit: int):
    return db.get_teiban(limit)


@app.get("/api/trend")
def get_trend(hr: int, limit: int):
    return db.get_trend(hr, limit)


@app.get("/api/hottrend")
def get_hottrend(hr: int, limit: int):
    return db.get_hottrend(hr, limit)


@app.get("/api/new")
def get_new(hr: int, limit: int):
    return db.get_new(hr, limit)


app.mount("/", MountFiles(directory="web/public", html=True), name="static")
