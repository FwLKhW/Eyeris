import subprocess
from pathlib import Path


def indexing(path: Path):
    subprocess.run(["bin/iie", "index", str(path)], check=False)


def indexing_extended(path: Path):
    subprocess.run(["bin/iie", "index", str(path), "-e"], check=False)


def generate_thumbnails(path: Path):
    subprocess.run(["bin/iie", "thumb", str(path)], check=False)
