from pathlib import Path
from pprint import pprint

from src.collection import Collection, CollectionManager

collections = CollectionManager()

print("Collection DB:", collections.db_path)

collection_schema = collections.add()

if collection_schema is not None:
    col = Collection(Path(collection_schema["path"]))
    col.indexing(clean=True)
    images = col.get_images({})

    print(f"Loaded {len(images)} images from {col.path}:")
    for i, img in enumerate(images):
        print(f"{i} {img['name']}")

    print("First image:")
    pprint(images[0], sort_dicts=False)
