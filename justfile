_:
    @just --list

dev:
    uv run app.py

build:
    uv run pyinstaller --clean --noconsole --onefile --add-data "ui:ui" app.py
