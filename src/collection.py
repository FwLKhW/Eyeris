import subprocess
from pathlib import Path

import numpy as np
import polars as pl

from src.color import hex_to_slint_color
from src.config import DOT_FOLDER
from src.log import get_logger
from src.utils import load_image

logger = get_logger("Collection")


class Collection:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.name
        self.csv_path = self.path / DOT_FOLDER / "index.csv"
        self.thumbnails_path = self.path / DOT_FOLDER / "thumbnails"

    def slint(self) -> dict:
        return {"name": self.name, "path": str(self.path)}

    def indexing(self) -> bool:
        result = subprocess.run(["bin/iie", "index", str(self.path)], check=False)
        return result.returncode == 0

    def indexing_extended(self) -> bool:
        result = subprocess.run(["bin/iie", "index", str(self.path), "-e"], check=False)
        return result.returncode == 0

    def generate_thumbnails(self) -> bool:
        result = subprocess.run(["bin/iie", "thumb", str(self.path)], check=False)
        return result.returncode == 0

    def get_thumbnail(self, hash: str) -> np.ndarray | None:
        return load_image(self.thumbnails_path / f"{hash}.png")

    def get_image(self, rel_path: str) -> np.ndarray | None:
        return load_image(self.path / rel_path)

    def get_images_data(self) -> list:
        q = pl.scan_csv(self.csv_path)
        df = q.collect()
        images = self._df_to_slint(df)

        return images

    def _df_to_slint(self, df: pl.DataFrame) -> list:
        def transform_item(item: dict) -> dict:
            item.pop("id")
            item["tags"] = item["tags"].split("|")
            item["colors"] = []
            for color_key in ["color_1", "color_2", "color_3", "color_4"]:
                if item.get(color_key):
                    item["colors"].append(hex_to_slint_color(item[color_key]))
                item.pop(color_key)
            return item

        df_filled = df.with_columns(
            [pl.col("tags").fill_null(""), pl.col("hash").fill_null("")]
        )
        raw_items = df_filled.to_dicts()
        transformed_items = list(map(transform_item, raw_items))

        return transformed_items
