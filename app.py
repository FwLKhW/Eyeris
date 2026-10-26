import sys
from pathlib import Path

import slint

ui_path = Path(__file__).parent / "slint"
sys.path.append(str(ui_path))


class App(slint.loader.app.App):
    def __init__(self) -> None:
        super().__init__()


async def main(app: slint.Component) -> None:
    app.show()


app = App()
slint.run_event_loop(main(app))
