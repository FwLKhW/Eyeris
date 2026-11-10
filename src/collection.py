import sqlite3
from pathlib import Path
from subprocess import run

from crossfiledialog import choose_folder, open_multiple


class Collection:
    def __init__(self, path: str | None = None):
        if path is None:
            path = choose_folder()

        self.path = Path(path)
        print(f"Open Collection: {self.path}")

        self.db = sqlite3.connect(self.path / "index.db")
        self.db.row_factory = sqlite3.Row

    def add_images(self):
        image_paths = open_multiple(
            filter={"Images": ["*.png", "*.jpg", "*.jpeg", "*.webp"]}
        )
        run(
            ["target/release/cli", str(self.path), "add", "images"] + image_paths,
            check=False,
        )

    def add_folder(self):
        image_folder_path = choose_folder()
        run(
            ["target/release/cli", str(self.path), "add", "folder", image_folder_path],
            check=False,
        )
