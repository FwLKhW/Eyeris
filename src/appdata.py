import os
import sqlite3
from pathlib import Path

import platformdirs


class AppData:
    def __init__(self):
        self.appdata_path = platformdirs.user_data_path() / "eyeris"
        os.makedirs(self.appdata_path, exist_ok=True)

        self.db = sqlite3.connect(self.appdata_path / "eyeris.db")
        self.db.row_factory = sqlite3.Row
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS collections (
                path    TEXT PRIMARY KEY
            )
        """)

    def get_collections(self) -> list[Path]:
        collections = self.db.execute("SELECT * FROM collections").fetchall()
        return [Path(p[0]) for p in collections]

    def upsert_collection(self, path: Path):
        self.db.execute(
            "INSERT INTO collections (path) VALUES (?)",
            (str(path.resolve()),),
        )


if __name__ == "__main__":
    pass
