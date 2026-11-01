# uv run python -m tests.manual.test_appdata

from pathlib import Path
from pprint import pp

from src.appdata import AppData

appdata = AppData()

appdata.upsert_collection(Path("fixtures/Example"))
appdata.upsert_collection(Path("fixtures/Example"))
appdata.upsert_collection(Path("~/Pictures"))
results = appdata.get_collections()

pp(results)
