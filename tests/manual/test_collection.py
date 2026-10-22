import json
from pathlib import Path
from pprint import pprint

from src.collection import Collection, CollectionManager

collections = CollectionManager()

print("Collection DB:", collections.db_path)

collections.clear()

with open(collections.db_path, "r") as f:
    txt = json.load(f)
    pprint(txt)

col = collections.add()
collections.add()

with open(collections.db_path, "r") as f:
    txt = json.load(f)
    pprint(txt)

if col is not None:
    col = Collection(Path(col["path"]))
    col.indexing()
    images = col.get_images()

    print(f"Load {len(images)} images from {col.path}")

    print("Head 3 images:")
    pprint(images[:3], sort_dicts=False)
