from pathlib import Path

import numpy as np
import slint
from PIL import Image


def load_image(path: Path) -> np.ndarray:
    return np.array(Image.open(path))


def to_slint(data):
    if isinstance(data, dict):
        return {k: to_slint(v) for k, v in data.items()}
    elif isinstance(data, list):
        return slint.ListModel([to_slint(item) for item in data])
    elif isinstance(data, np.ndarray):
        return slint.Image.load_from_array(data)
    else:
        return data
