_:
    @just --list

dev:
    uv run app.py

# uv run pyinstaller --clean --noconfirm --noconsole --onefile --add-data "ui;ui" --add-data "assets;assets" -i "assets/icon.ico" -n "eyeris" --version-file version.txt --distpath build --log-level ERROR app.py

build:
    uv run pyinstaller app.spec --clean --noconfirm --distpath build --log-level WARN
