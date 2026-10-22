import os
from pathlib import Path

from crossfiledialog import choose_folder
from slint import slint
from tinydb import TinyDB, where

from src.config import ALLOWED_IMAGE_EXTENSIONS, APPLICATION_DATA_PATH, DOT_FOLDER
from src.schema import CollectionSchema
from src.utils import index_image


class Collection:
    def __init__(self, path: Path) -> None:
        os.makedirs(path / DOT_FOLDER, exist_ok=True)
        self.path = path
        self.name = path.name
        self.db = TinyDB(self.path / DOT_FOLDER / "images.json", indent=4)

    def indexing(self):
        """Read/write images data and create thumbnail."""

        thumbnail_folder = self.path / DOT_FOLDER / "thumbnail"
        os.makedirs(thumbnail_folder, exist_ok=True)

        image_paths = [
            path
            for path in self.path.rglob("*")
            if path.is_file()
            and path.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS
            and not any(
                part.startswith(".")
                for part in path.relative_to(other=self.path).parts[:-1]
            )
        ]

        # TODO: dont index indexed images again
        for image_path in image_paths:
            image_data, thumbnail = index_image(image_path)
            thumbnail.save(thumbnail_folder / f"{image_data['id']}.png")
            self.db.upsert(image_data, where("id") == image_data["id"])

    def get_images(self):
        """Get IndexedImage[]"""

        with TinyDB(self.path / DOT_FOLDER / "images.json", indent=4) as db:
            images = db.all()
            return images

    def schema(self):
        return CollectionSchema(name=self.name, path=str(self.path))


class CollectionManager:
    def __init__(self) -> None:
        os.makedirs(APPLICATION_DATA_PATH, exist_ok=True)
        self.db_path = APPLICATION_DATA_PATH / "collection.json"
        self.db = TinyDB(self.db_path, indent=4)
        self.current_collection: Collection | None

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
