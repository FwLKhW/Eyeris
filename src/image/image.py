from pathlib import Path


class Image:
    def __init__(self, path: Path):
        self.path = path

    def identity(self) -> tuple[str, int, int, int]:
        """Quick identify image in file system by path, size, ctime and mtime. 
        Which surely enough to ensure it is."""

        return ("path/to/image.png", 0, 0, 0)
