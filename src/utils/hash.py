from blake3 import blake3
from PIL import Image


def hash_image(image_path: str) -> str:
    image = Image.open(image_path)
    image_rgb = image.convert("RGB")
    pixel_bytes = image_rgb.tobytes()
    pixel_hash = blake3(pixel_bytes).hexdigest()

    return pixel_hash


if __name__ == "__main__":
    print(hash_image("fixtures/images/kurisu.jpg"))
