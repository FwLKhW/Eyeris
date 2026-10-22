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
    def open_library(self, lib: str):
        print("Open Library:", lib)


def main():
    app = App()
    app.show()
    app.run()


if __name__ == "__main__":
    main()
