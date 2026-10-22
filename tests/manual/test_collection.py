from pathlib import Path
from pprint import pprint

from src.collection import Collection, CollectionManager

collections = CollectionManager()

print("Collection DB:", collections.db_path)

collections.clear()
print("List Collection:", collections.list())

col = collections.add()
collections.add()

print("List Collection:", collections.list())

if col is not None:
    col = Collection(Path(col["path"]))
    col.indexing()
    images = col.get_images()

    print(f"Loaded {len(images)} images from {col.path}:")
    for i, img in enumerate(images):
        print(f"{i} {img['name']}")

    print("First image:")
    pprint(images[0], sort_dicts=False)
