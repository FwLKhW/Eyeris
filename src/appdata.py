import os
import sqlite3
from pathlib import Path

from src.config import APPLICATION_DATA_PATH


class AppData:
    def __init__(self):
        os.makedirs(APPLICATION_DATA_PATH, exist_ok=True)

        self.db = sqlite3.connect(APPLICATION_DATA_PATH / "eyeris.db")
        self.db.row_factory = sqlite3.Row
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS collections (
                path    TEXT PRIMARY KEY
            )
        """)

    def get_collections(self) -> list[dict]:
        collections = self.db.execute("SELECT * FROM collections").fetchall()
        return [{"path": p[0], "name": Path(p[0]).name} for p in collections]

    def upsert_collection(self, path: Path):
        self.db.execute(
            "INSERT OR IGNORE INTO collections (path) VALUES (?)",
            (str(path.resolve()),),
        )
        self.db.commit()

    def clear_collection_history(self):
        self.db.execute("DELETE FROM collections")
        self.db.commit()


if __name__ == "__main__":
    pass
