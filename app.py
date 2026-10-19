import sys
from pathlib import Path

import slint

ui_path = Path(__file__).parent / "ui"
sys.path.append(str(ui_path))


class App(slint.loader.app.App):
    pass


def main():
    app = App()
    app.show()
    app.run()


if __name__ == "__main__":
    main()
