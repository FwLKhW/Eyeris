import os
from datetime import UTC, datetime
from pathlib import Path

from blake3 import blake3
from PIL import Image
from tinydb import TinyDB

from src.config import ALLOWED_IMAGE_EXTENSIONS, DOT_FOLDER, THUMBNAIL_SIZE
from src.schema import IndexedImage, Timestamps


def hash_image(image_path: Path) -> str:
    image = Image.open(image_path)
    image_rgb = image.convert("RGB")
    pixel_bytes = image_rgb.tobytes()
    pixel_hash = blake3(pixel_bytes).hexdigest()

    return pixel_hash


def index_image(image_path: Path) -> tuple[IndexedImage, Image.Image]:
    img = Image.open(image_path)

    indexed = IndexedImage(
        id=hash_image(image_path),
        name=image_path.name,
        path=str(image_path),
        size=image_path.stat().st_size,
        width=img.width,
        height=img.height,
        format=image_path.suffix[1:].upper(),
        timestamps=Timestamps(
            indexed=int(datetime.now(UTC).timestamp()),
            created=int(image_path.stat().st_ctime),
            modified=int(image_path.stat().st_mtime),
        ),
    )
    img.thumbnail((THUMBNAIL_SIZE, THUMBNAIL_SIZE))

    return (indexed, img)


def index_library(folder_path: Path):
    thumbnail_folder = folder_path / DOT_FOLDER / "thumbnail"
    os.makedirs(thumbnail_folder, exist_ok=True)

    db = TinyDB(folder_path / DOT_FOLDER / "images.json", indent=4)

    image_paths = [
        path
        for path in folder_path.rglob("*")
        if path.is_file()
        and path.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS
        and not any(
            part.startswith(".")
            for part in path.relative_to(other=folder_path).parts[:-1]
        )
    ]

    for image_path in image_paths:
        indexed, img = index_image(image_path)
        img.save(thumbnail_folder / f"{indexed['id']}.png")
        db.insert(indexed)


if __name__ == "__main__":
    from crossfiledialog import choose_folder

    index_library(Path(choose_folder()))
