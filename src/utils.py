from datetime import UTC, datetime
from pathlib import Path

import numpy as np
from blake3 import blake3
from colorthief import ColorThief
from PIL import Image
from slint import ListModel, slint

from src.config import THUMBNAIL_SIZE
from src.schema import IndexedImageSchema


def load_image(path: str) -> slint.Image:
    return slint.Image.load_from_array(np.array(Image.open(path)))


def hash_image(image_path: Path) -> str:
    """Pure function to hash an image using blake3."""

    image = Image.open(image_path)
    image_rgb = image.convert("RGB")
    pixel_bytes = image_rgb.tobytes()
    pixel_hash = blake3(pixel_bytes).hexdigest()

    return pixel_hash


def index_image(image_path: Path) -> tuple[IndexedImageSchema, Image.Image]:
    """Pure function to create indexed data and thumbnail for an image."""

    img = Image.open(image_path)

    rating = 0
    tags = []
    creator = ""
    description = ""

    indexed = IndexedImageSchema(
        id=hash_image(image_path),
        name=image_path.name,
        format=image_path.suffix[1:].upper(),
        path=str(image_path),
        size=image_path.stat().st_size,
        width=img.width,
        height=img.height,
        indexed=int(datetime.now(UTC).timestamp()),
        created=int(image_path.stat().st_ctime),
        modified=int(image_path.stat().st_mtime),
        rating=rating,
        tags=tags,
        creator=creator,
        description=description,
        palette=[],
    )
    img.thumbnail((THUMBNAIL_SIZE, THUMBNAIL_SIZE))

    return (indexed, img)


def get_color_palette(thumbnail_path: Path) -> list[tuple[int, int, int]]:
    """Get color palette. Should use thumbnail for speed."""

    color_thief = ColorThief(thumbnail_path)
    # dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=4, quality=4)

    return palette


def indexed_image_to_slint(img):
    def to_slint_color(rgb: tuple[int, int, int]) -> slint.Color:
        return slint.Color(
            {
                "red": rgb[0],
                "blue": rgb[1],
                "green": rgb[2],
            }
        )

    return {
        "id": img["id"],
        "path": img["path"],
        "name": img["name"],
        "format": img["format"],
        "size": img["size"],
        "width": img["width"],
        "height": img["height"],
        "indexed": img["indexed"],
        "created": img["created"],
        "modified": img["modified"],
        "rating": img["rating"],
        "tags": ListModel(img["tags"]),
        "creator": img["creator"],
        "description": img["description"],
        "palette": ListModel([to_slint_color(rgb) for rgb in img["palette"]]),
    }
