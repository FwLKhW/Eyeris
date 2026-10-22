import sys
from pathlib import Path

import slint
from slint import ListModel

from src.collection import CollectionManager

ui_path = Path(__file__).parent / "ui"
sys.path.append(str(ui_path))


class App(slint.loader.app.App):
    def __init__(self) -> None:
        super().__init__()
        self.collection_manager = CollectionManager()

    @slint.callback(global_name="Actions")
    def load_collection_list(self):
        self.CollectionState.collections = ListModel(self.collection_manager.list())

    @slint.callback(global_name="Actions")
    def add_collection(self):
        col = self.collection_manager.add()
        if col is None:
            return
        self.open_collection(col["path"])

    @slint.callback(global_name="Actions")
    def open_collection(self, path: str):
        col = self.collection_manager.load(Path(path))
        if col is None:
            return

        self.CollectionState.current_collection = col.schema()
        print(f"Open Collection '{col.name}' ({col.path})")

        self.GalleryState.images = ListModel(col.get_images())

    @slint.callback(global_name="Actions")
    def load_thumbnail(self, id: str):
        pass


def main():
    app = App()
    app.show()
    app.run()


if __name__ == "__main__":
    main()
