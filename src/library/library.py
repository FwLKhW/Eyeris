import os
from pathlib import Path
from typing import TypedDict

from crossfiledialog import choose_folder
from tinydb import TinyDB

from src.config import APPLICATION_DATA_PATH, LIBRARY_JSON_PATH

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
