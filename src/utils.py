from pathlib import Path

import numpy as np
import slint
from PIL import Image


def load_slint_image(path: Path) -> slint.Image:
    return slint.Image.load_from_array(np.array(Image.open(path)))


def to_slint(data):
    if isinstance(data, dict):
        return {k: to_slint(v) for k, v in data.items()}
    elif isinstance(data, list):
        return slint.ListModel([to_slint(item) for item in data])
    else:
        return data
