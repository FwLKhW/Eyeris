from datetime import UTC, datetime
from pathlib import Path

from blake3 import blake3
from PIL import Image

from src.config import THUMBNAIL_SIZE
from src.schema import IndexedImage


def hash_image(image_path: Path) -> str:
    """Pure function to hash an image using blake3."""

    image = Image.open(image_path)
    image_rgb = image.convert("RGB")
    pixel_bytes = image_rgb.tobytes()
    pixel_hash = blake3(pixel_bytes).hexdigest()

    return pixel_hash


def index_image(image_path: Path) -> tuple[IndexedImage, Image.Image]:
    """Pure function to create indexed data and thumbnail for an image."""

    img = Image.open(image_path)

    indexed = IndexedImage(
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
