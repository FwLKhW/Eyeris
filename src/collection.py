import sqlite3
import time
from pathlib import Path

import numpy as np

from src.color import dec_to_slint_color
from src.log import get_logger
from src.utils import load_image

logger = get_logger("Collection")


class Collection:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.db_path = self.path / "index.db"
        self.db: sqlite3.Connection | None = None
        self.images_path = self.path / "images"

    def get_image(self, hash: str, fullname: str) -> np.ndarray | None:
        return load_image(self.images_path / hash / fullname)

    def get_db(self) -> sqlite3.Connection:
        if not isinstance(self.db, sqlite3.Connection):
            self.db = sqlite3.connect(self.db_path)
            self.db.row_factory = sqlite3.Row
        return self.db

    def get_images_data(self, filters: dict | None = None) -> list:
        if not self.db_path.exists():
            return []

        cur = self.get_db().execute(self._get_query_by_filters(filters))

        rows = cur.fetchall()
        images = [self._row_to_dict(dict(row)) for row in rows]
        return images

    def tag(self, id: int, tags: list[str]):
        tags_str = "|".join(tags)
        self.get_db().execute(
            """
            INSERT INTO images (id, tags) VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET tags = excluded.tags
            """,
            (
                id,
                tags_str,
            ),
        )
        self.get_db().commit()

    def _get_query_by_filters(self, filters: dict | None = None) -> str:
        """Example:
        filters = {
            "search": "cat",
        }
        """

        query = "SELECT * FROM images"

        if filters is None or len(filters) == 0:
            return query

        conditions = []

        for key, value in filters.items():
            if key == "search":
                conditions.append(f"(name LIKE '%{value}%')")
            if key == "last_created":
                current_time_ms = time.time_ns() // 1_000_000
                conditions.append(f"(created > {current_time_ms - value})")

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        return query

    def _row_to_dict(self, item: dict) -> dict:
        item.pop("id")
        item["tags"] = item["tags"].split("|")
        item["colors"] = []
        for color_key in ["color_1", "color_2", "color_3", "color_4"]:
            if item.get(color_key):
                item["colors"].append(dec_to_slint_color(item[color_key]))
            item.pop(color_key)
        return item
