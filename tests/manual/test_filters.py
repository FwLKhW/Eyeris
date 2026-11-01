# uv run python -m tests.manual.test_filters

from pathlib import Path
from pprint import pp

from src.collection import Collection

collection = Collection(Path("fixtures/Example"))

results = collection.get_images_data(filters={"search": "D"})

pp(results)
