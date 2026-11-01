# uv run python -m tests.manual.test_appdata

from pathlib import Path
from pprint import pp

from src.appdata import AppData

appdata = AppData()

results = appdata.upsert_collection(Path("fixtures/Example"))
results = appdata.get_collections()

pp(results)
