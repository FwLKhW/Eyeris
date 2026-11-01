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

    def index_images(self, image_paths: list[Path]):
        if not image_paths:
            return

        images = []
        valid_paths = []

        for path in image_paths:
            try:
                img = Image.open(path).convert("RGB")
                images.append(img)
                valid_paths.append(path)
            except Exception as e:  # noqa: BLE001
                print(f"Skipping {path} due to load error: {e}")

        if not images:
            return

        embeddings = self.model.encode(
            images, normalize_embeddings=True, convert_to_numpy=True
        ).tolist()
        ids = [str(path.resolve()) for path in valid_paths]

        self.collection.upsert(ids=ids, embeddings=embeddings)

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
    pass
