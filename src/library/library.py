import os
from typing import TypedDict

from platformdirs import user_data_path
from tinydb import TinyDB

APPLICATION_DATA_PATH = user_data_path() / "eyeris"
LIBRARY_JSON_PATH = APPLICATION_DATA_PATH / "library.json"

os.makedirs(APPLICATION_DATA_PATH, exist_ok=True)

db = TinyDB(LIBRARY_JSON_PATH)


class Library(TypedDict):
    path: str
    name: str


def load_library_list():
    return db.all()


def add_library(lib: Library):
    db.insert(lib)


if __name__ == "__main__":
    from pprint import pprint

    add_library({"name": "Wallpapers", "path": "~/Pictures/Wallpapers"})
    add_library({"name": "Anime", "path": "~/Pictures/Anime"})
    add_library({"name": "Design", "path": "~/Pictures/Design"})

    pprint(load_library_list())
