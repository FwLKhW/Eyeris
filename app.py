from pathlib import Path

import slint


def main():
    ui_path = Path(__file__).parent / "ui"

    ui = slint.load_file(
        ui_path / "app.slint",
        library_paths={
            "ui": ui_path / "ui.slint",
        },
    )

    app = ui.App()
    app.show()
    app.run()


if __name__ == "__main__":
    main()
