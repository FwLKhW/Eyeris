from pathlib import Path

import slint

ui = slint.load_file(
    Path(__file__).parent / "../../ui/app.slint",
    library_paths={
        "ui": Path(__file__).parent / "../../ui/ui.slint",
    },
)


class MainWindow(ui.MainWindow):
    def __init__(self):
        super().__init__()


def main():
    main_window = MainWindow()
    main_window.show()
    main_window.run()


if __name__ == "__main__":
    main()
