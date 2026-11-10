import sqlite3
from pathlib import Path
from subprocess import run

import pandas as pd
from crossfiledialog import choose_folder, open_multiple

from src.ss import SS


class Collection:
    def __init__(self, path: str | None = None):
        if path is None:
            path = choose_folder()

        self.path = Path(path)
        print(f"Open Collection: {self.path}")

        self.db = sqlite3.connect(self.path / "index.db")
        self.db.row_factory = sqlite3.Row

        self.ss = SS(self.path / "embeddings")

    def add_images(self):
        image_paths = open_multiple(
            filter={"Images": ["*.png", "*.jpg", "*.jpeg", "*.webp"]}
        )
        if image_paths is None:
            return
        run(
            ["target/release/cli", str(self.path), "add", "images"] + image_paths,
            check=False,
        )

    def add_folder(self):
        image_folder_path = choose_folder()
        if image_folder_path is None:
            return
        run(
            ["target/release/cli", str(self.path), "add", "folder", image_folder_path],
            check=False,
        )

    def images_df(self) -> pd.DataFrame:
        df = pd.read_sql_query("SELECT * FROM images", self.db)

        df["id"] = df["id"].astype(str)

        base_path = f"{self.path}/images/"
        df["path"] = base_path + df["hash"] + "/" + df["fullname"]
        df["thumb_path"] = base_path + df["hash"] + "/thumbnail.png"

        return df
