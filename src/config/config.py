from platformdirs import user_data_path

APPLICATION_DATA_PATH = user_data_path() / "eyeris"
LIBRARY_JSON_PATH = APPLICATION_DATA_PATH / "library.json"
GALLERY_JSON_NAME = "gallery.json"

ALLOWED_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")
