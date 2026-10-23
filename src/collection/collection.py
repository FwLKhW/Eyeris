import operator
import os
import re
from functools import reduce
from pathlib import Path

from crossfiledialog import choose_folder
from slint import slint
from tinydb import Query, TinyDB, where

from src.config import ALLOWED_IMAGE_EXTENSIONS, APPLICATION_DATA_PATH, DOT_FOLDER
from src.schema import CollectionSchema
from src.utils import (
    get_color_palette,
    have_similar_color,
    index_image,
    indexed_image_to_slint,
    load_image,
)


class Collection:
    def __init__(self, path: Path) -> None:
        os.makedirs(path / DOT_FOLDER, exist_ok=True)
        self.path = path
        self.name = path.name
        self.db = TinyDB(self.path / DOT_FOLDER / "images.json", indent=4)
        self.thumbnail_folder = self.path / DOT_FOLDER / "thumbnail"
        os.makedirs(self.thumbnail_folder, exist_ok=True)
        self.Filter = Query()

    def indexing(self, clean=False):
        """Read/write images data and create thumbnail."""

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

        Img = Query()
        for image_path in image_paths:
            if not clean:
                matches = self.db.search(
                    Img.fragment(
                        {"path": str(image_path), "size": image_path.stat().st_size}
                    )
                )
                if len(matches) > 0:
                    continue

            image_data, thumbnail = index_image(image_path)

            thumbnail_path = self.thumbnail_folder / f"{image_data['id']}.png"
            thumbnail.save(self.thumbnail_folder / f"{image_data['id']}.png")

            palette = get_color_palette(thumbnail_path)
            image_data["palette"] = palette

            self.db.upsert(image_data, where("id") == image_data["id"])

    def clean_indexing(self):
        self.indexing(clean=True)

    def get_images(self, filters: dict):
        """Get IndexedImage[]"""

        queries = []

        if filters.get("name") is not None and len(filters["name"]) > 0:
            queries.append(
                self.Filter.name.search(filters["name"], flags=re.IGNORECASE)
            )

        if filters.get("types") is not None and filters["types"].lower() in [
            "jpg",
            "png",
            "webp",
        ]:
            queries.append(self.Filter.format == filters["types"].upper())

        if filters.get("shape") is not None:
            if filters["shape"] == "square":
                queries.append(lambda doc: doc.get("width", 0) == doc.get("height", 0))
            elif filters["shape"] == "landscape":
                queries.append(lambda doc: doc.get("width", 0) > doc.get("height", 0))
            elif filters["shape"] == "portrait":
                queries.append(lambda doc: doc.get("width", 0) < doc.get("height", 0))

        if filters.get("color") is not None:
            queries.append(
                self.Filter.palette.test(
                    have_similar_color,  # pyright: ignore[reportArgumentType]
                    filters["color"],
                    filters["color_distance"],
                )
            )

        final_query = None if len(queries) == 0 else reduce(operator.and_, queries)

        with TinyDB(self.path / DOT_FOLDER / "images.json", indent=4) as db:
            if final_query is None:
                images = db.all()
            else:
                images = db.search(final_query)
            print(f"Loaded {len(images)} images with query {final_query}")

            return [indexed_image_to_slint(i) for i in images]

    def schema(self):
        return CollectionSchema(name=self.name, path=str(self.path))

    def thumbnail(self, id: str) -> slint.Image:
        return load_image(str(self.thumbnail_folder / f"{id}.png"))


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
