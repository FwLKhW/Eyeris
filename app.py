import sys
from asyncio.threads import to_thread
from pathlib import Path

import slint
from crossfiledialog import choose_folder

from src.collection import Collection
from src.log import get_logger
from src.utils import to_slint

ui_path = Path(__file__).parent / "ui"
sys.path.append(str(ui_path))

logger = get_logger("Application")


class App(slint.loader.app.App):
    def __init__(self) -> None:
        super().__init__()
        self.collection: Collection | None = None

    @slint.callback(global_name="Action")
    async def open_collection(self):
        path = choose_folder()
        if path is None:
            return
        await self.open_collection_by_path(path)

    @slint.callback(global_name="Action")
    async def open_collection_by_path(self, path: str):
        self.collection = Collection(Path(path))

        logger.info(
            f"Open collection '{self.collection.name}' ({self.collection.path})"
        )

        self.State.collection = to_slint(self.collection.slint())

        self.State.indexing = True
        await to_thread(self.collection.indexing)
        self.State.indexing = False
        self.State.images = to_slint(self.collection.get_images_data())

        await to_thread(self.collection.indexing_extended)
        self.State.images = to_slint(self.collection.get_images_data())

        await to_thread(self.collection.generate_thumbnails)
        self.State.images = to_slint(self.collection.get_images_data())

    @slint.callback(global_name="Action")
    def get_thumbnail(self, hash: str):
        if self.collection is None:
            return
        return to_slint(self.collection.get_thumbnail(hash))

    @slint.callback(global_name="Action")
    def get_image(self, rel_path: str):
        if self.collection is None:
            return
        img = to_slint(self.collection.get_image(rel_path))
        return img


async def main(app: slint.Component) -> None:
    app.show()


logger.info("Start")

app = App()
slint.run_event_loop(main(app))

logger.info("Close")
