import asyncio
import sys
from pathlib import Path

import slint

from src.collection import CollectionManager

ui_path = Path(__file__).parent / "ui"
sys.path.append(str(ui_path))


class App(slint.loader.app.App):
    def __init__(self) -> None:
        super().__init__()
        self.collection_manager = CollectionManager()

    @slint.callback(global_name="Actions")
    def get_collection_list(self):
        return slint.ListModel(self.collection_manager.list())

    @slint.callback(global_name="Actions")
    def open_collection(self):
        col = self.collection_manager.add()
        if col is None:
            return
        self.open_collection(col["path"])

    @slint.callback(global_name="Actions")
    async def active_collection(self, path: str):
        col = self.collection_manager.load(Path(path))
        if col is None:
            return

        self.CollectionState.current_collection = col.schema()
        print(f"Open Collection '{col.name}' ({col.path})")

        self.CollectionState.indexing = True
        await asyncio.to_thread(col.indexing)
        self.CollectionState.indexing = False

        self.GalleryState.images = slint.ListModel(col.get_images(self.get_filters()))


async def main(app: slint.Component) -> None:
    app.show()


app = App()
slint.run_event_loop(main(app))
