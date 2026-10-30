import os
from pathlib import Path

from crossfiledialog import choose_folder
from tinydb import TinyDB, where

from src.collection import Collection
from src.config import APPLICATION_DATA_PATH
from src.log import get_logger
from src.schema import CollectionSchema

logger = get_logger("CollectionManager")


class CollectionManager:
    def __init__(self) -> None:
        os.makedirs(APPLICATION_DATA_PATH, exist_ok=True)
        self.db_path = APPLICATION_DATA_PATH / "collection.json"
        self.db = TinyDB(self.db_path, indent=4)
        self.active_collection: Collection | None = None

    def list(self):
        """List all Collection.

        Returns:
            list[CollectionSchema]
        """

        self.db.remove(where("path").map(lambda p: os.path.exists(p)) == False)
        return self.db.all()

    def open(self):
        """Open a folder dialog to choose Collection, then add to DB."""

        path = choose_folder()
        if path is None:
            return

        collection_data = CollectionSchema(name=Path(path).name, path=str(Path(path)))
        self.db.upsert(collection_data, where("path") == path)

        return collection_data

    def active(self, path: Path):
        """Load Collection by path."""

        libs = self.db.search(where("path").map(lambda p: Path(p) == path) == True)
        if len(libs) == 0:
            return
        self.active_collection = Collection(Path(libs[0]["path"]))

        return self.active_collection

    def truncate(self):
        """Clear database."""
        self.db.truncate()
