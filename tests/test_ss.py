from src.collection import Collection

collection = Collection()

images = collection.images_df()
images["id"] = images["id"].astype(str)
images = images.to_dict(orient="records")

collection.ss.index_images(images)
