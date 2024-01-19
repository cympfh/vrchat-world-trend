import time
import tomllib
from datetime import datetime, timedelta

from clients import Database, VRChat, VRCError

db = Database()
vrc = VRChat()


def main():
    # Reload config
    config = tomllib.load(open("conf.toml", "rb"))

    # Exploring new worlds
    names = config.get("world", {}).get("names", [])
    for name in names:
        try:
            params = config.get("world", {}).get(name)
            if not params:
                continue
            print("Exploring", name)
            ws = vrc.worlds(params)
            db.upsert_worlds(ws)
        except VRCError as err:
            print(err)

    worlds = db.worlds()
    print(f"we have {len(worlds)} worlds")

    # Check popularity
    for world_id in worlds:
        # print("Checking", world_id)
        last = db.last_checked(world_id)
        # print("last checked at:", last)
        limit = datetime.now() - timedelta(
            minutes=config.get("batch", {}).get("interval_min", 60)
        )
        if last and last > limit:
            # print("skip")
            continue
        print("update", world_id)
        try:
            w = vrc.world(world_id)
            if w is not None:
                try:
                    db.update_world_description(w)
                    db.insert_world_popularity(w)
                except Exception as err:
                    print(err)
        except VRCError:
            print("Delete", world_id)
            db.del_record(world_id)
        time.sleep(1.5)


while True:
    main()
    time.sleep(120)
