from pathlib import Path

from platformdirs import user_data_path

APPLICATION_DATA_PATH = user_data_path() / "eyeris"

DOT_FOLDER = ".eyeris"

EXAMPLE_COLLECTION_PATH = Path("fixtures/Example")
