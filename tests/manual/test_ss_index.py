from pathlib import Path

from crossfiledialog import choose_folder

from src.collection import Collection
from src.ss import SS

collection = Collection(Path(choose_folder()))

ss = SS(collection.path / ".eyeris" / "chroma")

images = collection.get_db().execute("SELECT path FROM images").fetchall()
image_paths = [(collection.path / img["path"]).resolve() for img in images]

print(f"Indexing {len(image_paths)} images...")
ss.index_images(image_paths)
