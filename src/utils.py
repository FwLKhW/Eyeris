from datetime import UTC, datetime
from pathlib import Path

import numpy as np
from blake3 import blake3
from colorthief import ColorThief
from PIL import Image
from slint import slint

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
    )
    img.thumbnail((THUMBNAIL_SIZE, THUMBNAIL_SIZE))

    return (indexed, img)


def get_color_pallete(thumbnail_path: Path) -> list[tuple[int]]:
    """Get color pallete. Should use thumbnail for speed."""

    color_thief = ColorThief(thumbnail_path)
    # dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=4, quality=4)

    return palette
