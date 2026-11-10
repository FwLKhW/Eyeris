from pathlib import Path

import chromadb

from src.embed import PEEmbed


class SS:
    emb = PEEmbed()

    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.chroma = self.client.get_or_create_collection(
            name="images", metadata={"hnsw:space": "cosine"}
        )

    def index_images(self, images_data: list[dict], batch_size: int = 16):
        """images_data: list[{id: str, path: str}]"""

        if not images_data:
            return

        indexed_count = 0
        total = len(images_data)
        print(f"Start indexing {total} images")
        for i in range(0, len(images_data), batch_size):
            batch = []
            for image_data in images_data[i : i + batch_size]:
                results = self.chroma.get(ids=[image_data["id"]], include=[])
                if results["ids"]:
                    continue
                batch.append(image_data)

            print(f"Batch {i} - {i + batch_size}: {len(batch)}/{batch_size}")

            if len(batch) > 0:
                ids = [image["id"] for image in batch]
                embeddings = [self.emb.image(image["path"]).tolist() for image in batch]
                self.chroma.upsert(ids=ids, embeddings=embeddings)

            indexed_count += len(batch)
            print(f"{indexed_count}/{total} images indexed")

    def search(self, text: str, thres: float = 0.25, limit: int = 50) -> list[str]:
        count = self.chroma.count()
        if count == 0:
            return []

        query_embedding = self.emb.text(text).tolist()
        n_results = min(count, limit)
        results = self.chroma.query(
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
