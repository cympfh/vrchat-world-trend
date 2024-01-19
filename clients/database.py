import sqlite3
from datetime import datetime, timedelta

from cachetools import TTLCache, cached
from vrchatapi.models import LimitedWorld

from util.timelib import hours, minutes, seconds


class Database:
    def __init__(self):
        self.con = sqlite3.connect("database.sqlite3", check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self._init_worlds()
        self._init_world_description()
        self._init_world_popularity()

    def _init_worlds(self):
        """
        ワールドのメタ情報

        基本的にはそうそう変わることがない情報をここに持つ
        説明文 (description) だけ情報ソースが別なのでテーブルを分ける
        """
        cur = self.con.cursor()
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS worlds (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    author_id TEXT,
                    author_name TEXT,
                    capacity INTEGER,
                    image_url TEXT,
                    updated_at DATETIME
                )
            """
        )
        cur.close()
        self.con.commit()

    def _init_world_description(self):
        """
        ワールドの説明文だけを持つテーブル
        """
        cur = self.con.cursor()
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS world_description (
                    id TEXT PRIMARY KEY,
                    description TEXT
                )
            """
        )
        cur.close()
        self.con.commit()

    def _init_world_popularity(self):
        """
        inserted_at はデータベース的にその行を追加した時刻
        """
        cur = self.con.cursor()
        cur.execute(
            """
                CREATE TABLE IF NOT EXISTS world_popularity (
                    world_id TEXT,
                    favorites INTEGER,
                    private_occupants INTEGER,
                    public_occupants INTEGER,
                    visits INTEGER,
                    inserted_at DATETIME
                )
            """
        )
        cur.close()
        self.con.commit()

    @cached(cache=TTLCache(maxsize=10, ttl=30))
    def worlds(self) -> list[str]:
        """持ってる world_id をすべて返す"""
        cur = self.con.cursor()
        cur.execute("SELECT DISTINCT id FROM worlds")
        rows = cur.fetchall()
        cur.close()
        self.con.commit()
        return [row["id"] for row in rows]

    @cached(cache=TTLCache(maxsize=10, ttl=seconds(20)))
    def last_updated(self) -> dict:
        cur = self.con.cursor()
        cur.execute(
            """
            SELECT MAX(inserted_at) AS dt
            FROM world_popularity
        """
        )
        row = cur.fetchone()
        cur.close()
        self.con.commit()
        return row

    def upsert_worlds(self, worlds: list[LimitedWorld]):
        values = [
            (
                world.id,
                world.name,
                world.author_id,
                world.author_name,
                world.capacity,
                world.image_url,
                world.updated_at,
            )
            for world in worlds
        ]
        cur = self.con.cursor()
        sql = """
            INSERT OR REPLACE INTO worlds (
                id,
                name,
                author_id,
                author_name,
                capacity,
                image_url,
                updated_at
            ) VALUES ( ?, ?, ?, ?, ?, ?, ? )
        """
        cur.executemany(sql, values)
        cur.close()
        self.con.commit()

    def update_world_description(self, world: dict):
        values = (
            world["id"],
            world["description"],
        )
        cur = self.con.cursor()
        sql = """
            INSERT OR REPLACE INTO world_description (
                id,
                description
            ) VALUES ( ?, ? )
        """
        cur.execute(sql, values)
        cur.close()
        self.con.commit()

    def insert_world_popularity(self, world: dict):
        values = (
            world["id"],
            world["favorites"],
            world["privateOccupants"],
            world["publicOccupants"],
            world["visits"],
            datetime.now(),
        )
        print("insert_world_popularity", values)
        cur = self.con.cursor()
        sql = """
            INSERT OR REPLACE INTO world_popularity (
                world_id,
                favorites,
                private_occupants,
                public_occupants,
                visits,
                inserted_at
            ) VALUES ( ?, ?, ?, ?, ?, ? )
        """
        cur.execute(sql, values)
        cur.close()
        self.con.commit()

    def last_checked(self, world_id: str) -> datetime | None:
        """最後のそのワールドを調べた日付"""
        cur = self.con.cursor()
        cur.execute(
            "SELECT MAX(inserted_at) AS dt FROM world_popularity WHERE world_id = ?",
            (world_id,),
        )
        row = cur.fetchone()
        dt = row["dt"]
        cur.close()
        self.con.commit()
        if dt:
            try:
                return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")
            except:
                return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        return None

    @cached(cache=TTLCache(maxsize=20, ttl=hours(6)))
    def get_teiban(self, hr: int, limit: int):
        """期間に訪れた人数ランキング

        期間付きの定番人気ワールド
        """
        dt = datetime.now() - timedelta(hours=hr)
        query = """
            WITH scores AS (
                SELECT
                    world_id,
                    AVG(private_occupants + public_occupants) AS score
                FROM
                    world_popularity
                WHERE
                    inserted_at >= ?
                GROUP BY
                    world_id
                ORDER BY score DESC
                LIMIT 200
            )
            SELECT
                world_id,
                score,
                name,
                author_id,
                author_name,
                capacity,
                image_url,
                updated_at,
                description
            FROM scores
            INNER JOIN worlds ON scores.world_id = worlds.id
            LEFT OUTER JOIN world_description ON scores.world_id = world_description.id
            LIMIT ?
        """
        cur = self.con.cursor()
        cur.execute(query, (dt, limit))
        rows = cur.fetchall()
        cur.close()
        self.con.commit()
        return rows

    @cached(cache=TTLCache(maxsize=20, ttl=minutes(10)))
    def get_hottrend(self, hr: int, limit: int):
        """期間内で得たファボのランキング

        パラメータは他 API も共通

        Parameters
        ----------
        hr
            この期間 (hours) について集計する
        limit
            返す件数
        """
        dt = datetime.now() - timedelta(hours=hr)
        query = f"""
            WITH scores_max AS (
                SELECT
                    world_id,
                    MAX(favorites) AS score_max
                FROM
                    world_popularity
                WHERE
                    inserted_at >= ?
                GROUP BY
                    world_id
            ),
            scores_min AS (
                SELECT
                    world_id,
                    MAX(favorites) AS score_min
                FROM
                    world_popularity
                WHERE
                    inserted_at < ?
                GROUP BY
                    world_id
                HAVING
                    MAX(favorites) > 0
            ),
            scores AS (
                SELECT
                    scores_max.world_id,
                    (scores_max.score_max - scores_min.score_min) / pow(scores_min.score_min, 0.8) AS score,
                    scores_max.score_max,
                    scores_min.score_min
                FROM scores_max
                INNER JOIN scores_min ON scores_max.world_id = scores_min.world_id
            )
            SELECT
                world_id,
                score,
                score_max,
                score_min,
                name,
                author_id,
                author_name,
                capacity,
                image_url,
                updated_at,
                description
            FROM scores
            INNER JOIN worlds ON scores.world_id = worlds.id
            LEFT OUTER JOIN world_description ON scores.world_id = world_description.id
            ORDER BY score DESC
            LIMIT ?
        """
        cur = self.con.cursor()
        cur.execute(query, (dt, dt, limit))
        rows = cur.fetchall()
        cur.close()
        self.con.commit()
        return rows

    @cached(cache=TTLCache(maxsize=20, ttl=minutes(10)))
    def get_featured(self, hr: int, limit: int):
        """信頼区間割合で来てる人数が多いもの

        与えられた期間で観測値 (来てる人数) の平均 mu, 標準偏差 sigma を求める
        [mu-sigma, mu+sigma] の区間を [-100, 100] に写す (アフィン変換)
        最新の観測値を写した先で高い順を返す
        """
        dt = datetime.now() - timedelta(hours=hr)
        query = """
WITH scores_avg AS (
    SELECT
        world_id,
        AVG(private_occupants + public_occupants) AS score
    FROM
        world_popularity
    WHERE
        inserted_at >= ?
        AND (private_occupants + public_occupants) > 0
    GROUP BY
        world_id
    HAVING score > 1
),

scores_var AS (
    SELECT
        world_popularity.world_id,
        POW(AVG(POW(private_occupants + public_occupants - scores_avg.score, 2)), 0.5) AS score
    FROM
        world_popularity
    INNER JOIN scores_avg ON world_popularity.world_id = scores_avg.world_id
    WHERE
        inserted_at >= ?
        AND (private_occupants + public_occupants) > 0
    GROUP BY
        world_popularity.world_id
    HAVING score > 0
),

scores_latest AS (
    SELECT
        world_id,
        score,
        inserted_at
    FROM (
        SELECT 
            world_id,
            private_occupants + public_occupants AS score,
            inserted_at,
            ROW_NUMBER() OVER (PARTITION BY world_id ORDER BY inserted_at DESC) AS rn
        FROM
            world_popularity
        WHERE
            inserted_at >= ?
            AND (private_occupants + public_occupants) > 0
    )
    WHERE
        rn = 1
        AND score >= 6
)

SELECT
    scores_latest.world_id,
    100 * (scores_latest.score - scores_avg.score) / scores_var.score AS score,
    scores_latest.score AS score_latest,
    scores_avg.score AS score_avg,
    scores_var.score AS score_var,
    worlds.name,
    worlds.author_id,
    worlds.author_name,
    worlds.capacity,
    worlds.image_url,
    worlds.updated_at,
    world_description.description
FROM scores_latest
INNER JOIN scores_avg ON scores_latest.world_id = scores_avg.world_id
INNER JOIN scores_var ON scores_latest.world_id = scores_var.world_id
INNER JOIN worlds ON scores_latest.world_id = worlds.id
LEFT OUTER JOIN world_description ON scores_latest.world_id = world_description.id
ORDER BY score DESC
LIMIT ?
        """
        cur = self.con.cursor()
        cur.execute(query, (dt, dt, dt, limit))
        rows = cur.fetchall()
        cur.close()
        self.con.commit()
        return rows

    @cached(cache=TTLCache(maxsize=20, ttl=minutes(10)))
    def get_world_info(self, world_id: str):
        """ワールドのメタ情報"""
        cur = self.con.cursor()
        cur.execute(
            """
            SELECT
                worlds.id,
                name,
                author_id,
                author_name,
                capacity,
                image_url,
                updated_at,
                description
            FROM worlds
            INNER JOIN world_description
                ON worlds.id = world_description.id
            WHERE
                worlds.id = ?
        """,
            (world_id,),
        )
        w = cur.fetchone()
        return w

    @cached(cache=TTLCache(maxsize=20, ttl=minutes(10)))
    def get_world_history(self, world_id: str, limit: int):
        """ワールドの popularity の観測履歴"""
        cur = self.con.cursor()
        cur.execute(
            """
            SELECT
                favorites,
                private_occupants,
                public_occupants,
                visits,
                inserted_at AS dt
            FROM world_popularity
            WHERE
                world_id = ?
                AND ( private_occupants + public_occupants ) > 0
            ORDER BY inserted_at DESC
            LIMIT ?
            """,
            (world_id, limit),
        )
        return cur.fetchall()

    def get_kaso_worlds(self, limit: int, days: int):
        """過疎なワールドを列挙する

        Parameters
        ----------
        limit
            最大で来てる人数がコレ以下
        days
            調べる期間
        """
        dt = datetime.now() - timedelta(days=days)
        cur = self.con.cursor()
        cur.execute(
            """
            SELECT
                world_id,
                worlds.name,
                MAX(private_occupants + public_occupants) AS score
            FROM world_popularity
            INNER JOIN worlds ON world_popularity.world_id = worlds.id
            WHERE
                inserted_at >= ?
            GROUP BY world_id
            HAVING
                score <= ?
            """,
            (dt, limit),
        )
        return cur.fetchall()

    def del_record(self, world_id: str):
        """関わるレコードをすべて消す"""
        cur = self.con.cursor()
        cur.execute(
            "DELETE FROM worlds WHERE id = ?",
            (world_id,),
        )
        cur.execute(
            "DELETE FROM world_description WHERE id = ?",
            (world_id,),
        )
        cur.execute(
            "DELETE FROM world_popularity WHERE world_id = ?",
            (world_id,),
        )
        cur.close()
        self.con.commit()
