import subprocess
from pathlib import Path

from slint import slint

from src.config import DOT_FOLDER
from src.log import get_logger
from src.schema import CollectionSchema
from src.utils import load_slint_image

logger = get_logger("Collection")


class Collection:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.csv_path = self.path / DOT_FOLDER / "index.csv"
        self.thumbnails_path = self.path / DOT_FOLDER / "thumbnails"

    def indexing(self) -> bool:
        result = subprocess.run(["bin/iie", "index", str(self.path)], check=False)
        return result.returncode == 0

    def indexing_extended(self) -> bool:
        result = subprocess.run(["bin/iie", "index", str(self.path), "-e"], check=False)
        return result.returncode == 0

    def thumbnailing(self) -> bool:
        result = subprocess.run(["bin/iie", "thumb", str(self.path)], check=False)
        return result.returncode == 0

    def get_images(self):
        """Get IndexedImage[]"""
        return []

    def schema(self):
        return CollectionSchema(name=self.name, path=str(self.path))

    def thumbnail(self, hash: str) -> slint.Image:
        return load_slint_image(self.thumbnails_path / f"{hash}.png")
