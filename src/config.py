from platformdirs import user_data_path

APPLICATION_DATA_PATH = user_data_path() / "eyeris"

DOT_FOLDER = ".eyeris"

ALLOWED_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")

THUMBNAIL_SIZE = 512
