import sqlite3
from datetime import datetime, timedelta

from vrchatapi.models import LimitedWorld, World


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

    def worlds(self) -> list[str]:
        """持ってる world_id をすべて返す"""
        cur = self.con.cursor()
        cur.execute("SELECT DISTINCT id FROM worlds")
        rows = cur.fetchall()
        cur.close()
        self.con.commit()
        return [row["id"] for row in rows]

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

    def update_world_description(self, world: World):
        values = (
            world.id,
            world.description,
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

    def insert_world_popularity(self, world: World):
        values = (
            world.id,
            world.favorites,
            world.private_occupants,
            world.public_occupants,
            world.visits,
            datetime.now(),
        )
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
            return datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f")
        return None

    def get_teiban(self, limit: int):
        """今までに訪れた人数ランキング

        定番の人気ワールド
        """
        query = """
            WITH scores AS (
                SELECT
                    world_id,
                    MAX(visits) / 1000.0 AS score
                FROM
                    world_popularity
                GROUP BY
                    world_id
                ORDER BY score DESC
                LIMIT ?
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
        """
        cur = self.con.cursor()
        cur.execute(query, (limit,))
        rows = cur.fetchall()
        cur.close()
        self.con.commit()
        return rows

    def get_trend(self, hr: int, limit: int):
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
                LIMIT ?
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
        """
        cur = self.con.cursor()
        cur.execute(query, (dt, limit))
        rows = cur.fetchall()
        cur.close()
        self.con.commit()
        return rows

    def get_hottrend(self, hr: int, limit: int):
        """期間内で得たファボ数のランキング"""
        dt = datetime.now() - timedelta(hours=hr)
        query = """
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
            ),
            scores AS (
                SELECT
                    scores_max.world_id,
                    scores_max.score_max - scores_min.score_min AS score,
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

    def get_featured(self, hr: int, limit: int):
        """期間に訪れるようになった割合ランキング

        上り傾向の強いもの
        """
        dt = datetime.now() - timedelta(hours=hr)
        query = """
            WITH scores_recent AS (
                SELECT
                    world_id,
                    AVG(private_occupants + public_occupants) AS score
                FROM
                    world_popularity
                WHERE
                    inserted_at >= ?
                GROUP BY
                    world_id
            ),
            scores_all AS (
                SELECT
                    world_id,
                    AVG(private_occupants + public_occupants) AS score
                FROM
                    world_popularity
                WHERE
                    world_id IN (SELECT world_id FROM scores_recent)
                GROUP BY
                    world_id
            ),
            scores AS (
                SELECT
                    scores_recent.world_id,
                    scores_recent.score AS score_recent,
                    scores_all.score AS score_all,
                    (scores_recent.score / scores_all.score - 1) * 100 AS score
                FROM scores_recent
                INNER JOIN scores_all ON scores_recent.world_id = scores_all.world_id
                WHERE (scores_recent.score / scores_all.score) > 1.0
            )
            SELECT
                world_id,
                score,
                score_recent,
                score_all,
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
        cur.execute(query, (dt, limit))
        rows = cur.fetchall()
        cur.close()
        self.con.commit()
        return rows

    def get_new(self, hr: int, limit: int):
        """新しく発見したワールドの中でのランキング"""
        dt = datetime.now() - timedelta(hours=hr)
        query = """
            WITH scores_recent AS (
                SELECT
                    world_id,
                    AVG(private_occupants + public_occupants) AS score
                FROM
                    world_popularity
                WHERE
                    inserted_at > ?
                GROUP BY
                    world_id
                ORDER BY score DESC
            ),
            old_worlds AS (
                SELECT DISTINCT world_id
                FROM
                    world_popularity
                WHERE
                    inserted_at < ?
            ),
            scores AS (
                SELECT
                    world_id,
                    score
                FROM scores_recent
                WHERE
                    world_id NOT IN ( SELECT world_id FROM old_worlds )
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
            ORDER BY score DESC
            LIMIT ?
        """
        cur = self.con.cursor()
        cur.execute(query, (dt, dt, limit))
        rows = cur.fetchall()
        cur.close()
        self.con.commit()
        return rows
