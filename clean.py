import click

from clients.database import Database


@click.command()
@click.option("-n", type=int, default=2)
@click.option("--days", type=int, default=31)
@click.option("--dry-run", "-N", is_flag=True, default=False)
def main(n: int, days: int, dry_run: bool):
    """
    直近 days 日を見たとき,
    来てる人数が最大で n 人以下しか得られてないワールドを削除
    """
    db = Database()
    ws = db.worlds()
    print(f"We have {len(ws)} worlds")

    ws = db.get_kaso_worlds(n, days)
    print(f"Found {len(ws)} kaso worlds")
    for w in ws:
        print("deleting", dict(w))
        if not dry_run:
            db.del_record(dict(w)["world_id"])


if __name__ == "__main__":
    main()
