import os
import subprocess
from pathlib import Path

from crossfiledialog import choose_folder
from slint import slint
from tinydb import TinyDB, where

from src.config import APPLICATION_DATA_PATH, DOT_FOLDER
from src.schema import CollectionSchema
from src.utils import load_image


class Collection:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.thumbnail_folder = self.path / DOT_FOLDER / "thumbnails"

    def indexing(self) -> bool:
        result = subprocess.run(
            ["bin/image-indexing-engine", str(self.path), "-ip"], check=False
        )
        return result.returncode == 0

    def thumbnailing(self) -> bool:
        result = subprocess.run(
            ["bin/image-indexing-engine", str(self.path), "-t"], check=False
        )
        return result.returncode == 0

    def get_images(self, filters: dict):
        """Get IndexedImage[]"""
        return []

    def schema(self):
        return CollectionSchema(name=self.name, path=str(self.path))

    def thumbnail(self, hash: str) -> slint.Image:
        return load_image(str(self.thumbnail_folder / f"{hash}.png"))


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
