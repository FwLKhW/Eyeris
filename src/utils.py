import math
from pathlib import Path

import numpy as np
from PIL import Image
from slint import slint


def load_slint_image(path: Path) -> slint.Image:
    return slint.Image.load_from_array(np.array(Image.open(path)))


def have_similar_color(palette, target_color, max_distance=0.2):
    if not palette:
        return False

    for color in palette:
        distance = math.sqrt(
            (color[0] - target_color[0]) ** 2
            + (color[1] - target_color[1]) ** 2
            + (color[2] - target_color[2]) ** 2
        )
        if distance <= max_distance * 255:
            return True

    return False
