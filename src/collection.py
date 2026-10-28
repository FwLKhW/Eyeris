import os
import sqlite3
import subprocess
from pathlib import Path

from crossfiledialog import choose_folder
from slint import slint
from tinydb import TinyDB, where

from src.config import APPLICATION_DATA_PATH, DOT_FOLDER
from src.schema import CollectionSchema
from src.utils import load_slint_image


class Collection:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.image_db_path = self.path / DOT_FOLDER / "images.db"
        self.thumbnail_folder_path = self.path / DOT_FOLDER / "thumbnails"

    def _run_indexing(self, args: list[str]) -> bool:
        result = subprocess.run(
            ["bin/image-indexing-engine", str(self.path)] + args, check=False
        )
        return result.returncode == 0

    def indexing(self, force=False) -> bool:
        if not force and self.image_db_path.exists():
            return True

        return self._run_indexing(["-ip"])

    def force_indexing(self) -> bool:
        return self.indexing(True)

    def thumbnailing(self, force=False) -> bool:
        if not force and self.thumbnail_folder_path.exists():
            return True

        return self._run_indexing(["-t"])

    def force_thumbnailing(self) -> bool:
        return self.thumbnailing(True)

    def get_images(self):
        """Get IndexedImage[]"""

        self.image_db = sqlite3.connect(f"file:{self.image_db_path}?mode=ro", uri=True)
        images = self.image_db.execute("SELECT * FROM images").fetchall()

        return images

    def schema(self):
        return CollectionSchema(name=self.name, path=str(self.path))

    def thumbnail(self, hash: str) -> slint.Image:
        return load_slint_image(self.thumbnail_folder_path / f"{hash}.png")


class CollectionManager:
    def __init__(self) -> None:
        os.makedirs(APPLICATION_DATA_PATH, exist_ok=True)
        self.db_path = APPLICATION_DATA_PATH / "collection.json"
        self.db = TinyDB(self.db_path, indent=4)
        self.current_collection: Collection | None = None

    def add(self):
        """Open a folder dialog to choose Collection, then add to DB."""

        path = choose_folder()
        if path is None:
            return

        collection_data = CollectionSchema(name=Path(path).name, path=str(Path(path)))
        self.db.upsert(collection_data, where("path") == path)

        return collection_data

    def load(self, path: Path):
        """Load Collection by path."""

        libs = self.db.search(where("path").map(lambda p: Path(p) == path) == True)
        if len(libs) == 0:
            return
        self.current_collection = Collection(Path(libs[0]["path"]))

        return self.current_collection

    def list(self):
        """List all Collection.

        Returns:
            list[CollectionSchema]
        """

        self.db.remove(where("path").map(lambda p: os.path.exists(p)) == False)
        return self.db.all()

    def clear(self):
        """Clear database."""
        self.db.truncate()
