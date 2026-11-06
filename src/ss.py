from pathlib import Path

import chromadb
from PIL import Image
from sentence_transformers import SentenceTransformer


class SS:
    model_id: str = "sentence-transformers/clip-ViT-B-32"

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.model = SentenceTransformer(self.model_id)
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(
            name="images", metadata={"hnsw:space": "cosine"}
        )

    def test(self):
        self.collection.upsert(ids=["999"], embeddings=[[1] * 512])

    def index_images(self, images_data: list[dict], batch_size: int = 32):
        """images_data: list[{id: str, path: Path}]"""

        if not images_data:
            return

        cnt = 0
        total = len(images_data)
        for i in range(0, len(images_data), batch_size):
            batch_images = images_data[i : i + batch_size]
            images = []
            valid_paths = []

            for batch_image in batch_images:
                try:
                    img = Image.open(batch_image["path"]).convert("RGB")
                    images.append(img)
                    valid_paths.append(batch_image)
                except Exception as e:  # noqa: BLE001
                    print(f"Skipping {batch_image['path']} due to load error: {e}")

            if not images:
                continue

            embeddings = self.model.encode(
                images, normalize_embeddings=True, convert_to_numpy=True
            ).tolist()
            ids = [batch_image["id"] for batch_image in batch_images]

            print(ids, len(embeddings))
            self.collection.upsert(ids=ids, embeddings=embeddings)

            cnt += len(ids)
            print(f"{cnt}/{total} images indexed")

    def search(self, text: str, thres: float = 0.25, limit: int = 50) -> list[Path]:
        count = self.collection.count()
        if count == 0:
            return []

        query_embedding = self.model.encode(
            text, normalize_embeddings=True, convert_to_numpy=True
        ).tolist()
        n_results = min(count, limit)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["distances"],
        )

        matched_paths = []
        if results["distances"] and results["ids"]:
            distances = results["distances"][0]
            matched_ids = results["ids"][0]

            for dist, path_str in zip(distances, matched_ids):
                similarity = 1.0 - dist
                if similarity >= thres:
                    matched_paths.append(Path(path_str))

        return matched_paths


if __name__ == "__main__":
    import sqlite3

    from crossfiledialog import choose_folder

    collection_path = Path(choose_folder())
    ss = SS(collection_path / "chroma")
    ss.test()

    index_db = sqlite3.connect(collection_path / "index.db")
    index_db.row_factory = sqlite3.Row

    images = index_db.execute("SELECT id, hash, fullname FROM images").fetchall()
    images = [
        {
            "id": str(img["id"]),
            "path": collection_path / "images" / img["hash"] / img["fullname"],
        }
        for img in images
    ]

    # ss.index_images(images)

    # from pprint import pp

    # queries = [
    #     "Airplane",
    #     "A picture of the moon",
    #     "Thunder storm",
    #     "Flowers",
    #     "A picture of forest",
    #     "Leaf",
    # ]

    # for query in queries:
    #     print(query)
    #     pp(ss.search(query, limit=3))
    #     print()
