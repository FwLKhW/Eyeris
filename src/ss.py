from pathlib import Path

import chromadb

from src.embed import PEEmbed


class SS:
    pe = PEEmbed()

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(
            name="images", metadata={"hnsw:space": "cosine"}
        )

    def index_images(self, images_data: list[dict], batch_size: int = 32):
        """images_data: list[{id: str, path: str}]"""

        if not images_data:
            return

        cnt = 0
        total = len(images_data)
        print(f"Start indexing {total} images")
        for i in range(0, len(images_data), batch_size):
            batch_images = images_data[i : i + batch_size]

            ids = [batch_image["id"] for batch_image in batch_images]
            embeddings = [
                self.pe.image(image["path"]).tolist() for image in batch_images
            ]

            self.collection.upsert(ids=ids, embeddings=embeddings)

            cnt += len(ids)
            print(f"{cnt}/{total} images indexed")

    def search(self, text: str, thres: float = 0.25, limit: int = 50) -> list[str]:
        count = self.collection.count()
        if count == 0:
            return []

        query_embedding = self.pe.text(text).tolist()
        n_results = min(count, limit)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["distances"],
        )

        matched_ids = []
        if results["distances"] and results["ids"]:
            distances = results["distances"][0]
            ids = results["ids"][0]

            for dist, path_str in zip(distances, ids):
                similarity = 1.0 - dist
                if similarity >= thres:
                    matched_ids.append(path_str)

        return matched_ids


if __name__ == "__main__":
    pass
