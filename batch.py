import os
import time
import tomllib
from datetime import datetime, timedelta
from typing import cast

from clients import Database, VRChat

db = Database()
vrc = VRChat(
    username=cast(str, os.getenv("VRCHAT_USER")),
    password=cast(str, os.getenv("VRCHAT_PASSWORD")),
)


def main():
    # Reload config
    config = tomllib.load(open("conf.toml", "rb"))

    # Exploring new worlds
    names = config.get("world", {}).get("names", [])
    for name in names:
        params = config.get("world", {}).get(name)
        if not params:
            continue
        print("Exploring", name)
        ws = vrc.worlds(params)
        db.upsert_worlds(ws)

    worlds = db.worlds()
    print(f"we have {len(worlds)} worlds")

    # Check popularity
    for world_id in worlds:
        print("Checking", world_id)
        last = db.last_checked(world_id)
        print("last checked at:", last)
        limit = datetime.now() - timedelta(
            minutes=config.get("batch", {}).get("interval_min", 60)
        )
        if last and last > limit:
            print("skip")
            continue
        print("update")
        w = vrc.world(world_id)
        if w is not None:
            db.update_world_description(w)
            db.insert_world_popularity(w)
        time.sleep(1)


while True:
    main()
    time.sleep(600)
