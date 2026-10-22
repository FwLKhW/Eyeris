import os
from pathlib import Path

from crossfiledialog import choose_folder
from tinydb import TinyDB, where

from src.config import APPLICATION_DATA_PATH
from src.schema import Library

os.makedirs(APPLICATION_DATA_PATH, exist_ok=True)

db = TinyDB(APPLICATION_DATA_PATH / "library.json", indent=4)


def open_library_chooser():
    folder_path = choose_folder("Open a folder as Library")
    if folder_path is None:
        return None

    name = Path(folder_path).name
    db.upsert(Library(name=name, path=folder_path), where("path") == folder_path)

    return folder_path


def load_library_list():
    db.remove(where("path").map(lambda p: os.path.exists(p)) == False)
    return db.all()


def select_library_by_path(path: str):
    return db.search(where("path") == path)[0]


if __name__ == "__main__":
    pass
