import os
from pathlib import Path
from typing import TypedDict

from crossfiledialog import choose_folder
from platformdirs import user_data_path
from tinydb import TinyDB

APPLICATION_DATA_PATH = user_data_path() / "eyeris"
LIBRARY_JSON_PATH = APPLICATION_DATA_PATH / "library.json"

os.makedirs(APPLICATION_DATA_PATH, exist_ok=True)

db = TinyDB(LIBRARY_JSON_PATH)


class Library(TypedDict):
    path: str
    name: str


def open_library():
    folder_path = choose_folder("Open a folder as library")
    if folder_path is None:
        return None

    name = Path(folder_path).name
    add_library(Library(name=name, path=folder_path))

    return folder_path


def load_library_list():
    return db.all()


def add_library(lib: Library):
    db.insert(lib)


if __name__ == "__main__":
    pass
