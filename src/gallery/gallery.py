from pathlib import Path

from crossfiledialog import choose_folder
from slint import ListModel

images = ListModel([])


def load_gallery(folder_path: Path):
    pass


if __name__ == "__main__":
    load_gallery(Path(choose_folder()))
