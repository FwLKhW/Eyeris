import sys
from asyncio.threads import to_thread
from pathlib import Path

import slint

from src.collection_manager import CollectionManager
from src.log import get_logger

ui_path = Path(__file__).parent / "ui"
sys.path.append(str(ui_path))

logger = get_logger("Application")


class App(slint.loader.app.App):
    def __init__(self) -> None:
        super().__init__()
        self.collection_manager = CollectionManager()

    @slint.callback(global_name="Actions")
    def get_collection_list(self):
        return slint.ListModel(self.collection_manager.list())

    @slint.callback(global_name="Actions")
    def open_collection(self):
        col = self.collection_manager.open()
        if col is None:
            return
        self.active_collection(col["path"])

    @slint.callback(global_name="Actions")
    async def active_collection(self, path: str):
        col = self.collection_manager.active(Path(path))
        if col is None:
            return

        logger.info(f"Open Collection '{col.name}' ({col.path})")

        self.CollectionState.current_collection = col.schema()

        self.CollectionState.indexing = True
        await to_thread(col.indexing)
        self.CollectionState.indexing = False

        await to_thread(col.indexing_extended)
        await to_thread(col.thumbnailing)


async def main(app: slint.Component) -> None:
    app.show()


logger.info("Start")

app = App()
slint.run_event_loop(main(app))

logger.info("Close")
