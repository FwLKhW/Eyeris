import sys
from pathlib import Path

import slint
from slint import ListModel

from src import library

ui_path = Path(__file__).parent / "ui"
sys.path.append(str(ui_path))


class App(slint.loader.app.App):
    def __init__(self) -> None:
        super().__init__()
        self.libraries = ListModel(library.load_library_list())

    @slint.callback(global_name="Actions")
    def load_library_list(self):
        self.libraries = ListModel(library.load_library_list())
        self.LibraryState.libraries = self.libraries

    @slint.callback(global_name="Actions")
    def open_library_chooser(self):
        lib = library.open_library_chooser()
        if lib is None:
            return
        self.open_library(lib)

    @slint.callback(global_name="Actions")
    def open_library(self, path: str):
        self.LibraryState.library = library.select_library_by_path(path)
        print("Open Library:", path)
        # TODO

    @slint.callback(global_name="Actions")
    def load_thumbnail(self, id: str):
        pass


def main():
    app = App()
    app.show()
    app.run()


if __name__ == "__main__":
    main()
