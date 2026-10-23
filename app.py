import asyncio
import sys
from pathlib import Path

import slint
from slint import ListModel

from src import utils
from src.collection import CollectionManager

ui_path = Path(__file__).parent / "ui"
sys.path.append(str(ui_path))


class App(slint.loader.app.App):
    def __init__(self) -> None:
        super().__init__()
        self.collection_manager = CollectionManager()

    @slint.callback(global_name="Actions")
    def load_image(self, path: str):
        return utils.load_image(path)

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
    async def open_collection(self, path: str):
        col = self.collection_manager.load(Path(path))
        if col is None:
            return

        self.CollectionState.current_collection = col.schema()
        print(f"Open Collection '{col.name}' ({col.path})")

        self.CollectionState.indexing = True
        await asyncio.to_thread(col.indexing)
        self.CollectionState.indexing = False

        self.GalleryState.images = ListModel(col.get_images(self.get_filters()))

    @slint.callback(global_name="Actions")
    def load_thumbnail(self, id: str):
        if self.collection_manager.current_collection is None:
            return
        return self.collection_manager.current_collection.thumbnail(id)

    @slint.callback(global_name="Actions")
    def apply_filters(self):
        if self.collection_manager.current_collection is None:
            return

        self.GalleryState.images = ListModel(
            self.collection_manager.current_collection.get_images(self.get_filters())
        )

    def get_filters(self):
        return {
            "types": self.FilterState.types.value,
            "shape": self.FilterState.shape.value,
        }


async def main(app: slint.Component) -> None:
    app.show()


app = App()
slint.run_event_loop(main(app))
