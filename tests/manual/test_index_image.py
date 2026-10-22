from pathlib import Path
from pprint import pprint

from crossfiledialog import open_file

from src.utils import index_image

image = open_file(filter=["*.jpg", "*.jpeg", "*.png", "*.webp"])
if image is not None:
    data, thumb = index_image(Path(image))

    pprint(data, sort_dicts=False)
    thumb.show()
