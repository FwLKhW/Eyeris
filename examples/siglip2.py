from transformers import pipeline


class SemanticSearch:
    pipeline = pipeline(
        task="zero-shot-image-classification",
        model="google/siglip2-base-patch16-224",
        device=0,
    )

    def match(self, img: str, labels: list[str]):
        results = self.pipeline(img, candidate_labels=labels)
        return results


if __name__ == "__main__":
    ss = SemanticSearch()
    labels = ["an art of warplane", "abstract shapes like rectangle, circle"]
    imgs = [
        "fixtures/imgs/dinosaur.png",
        "fixtures/imgs/fighters.jpg",
        "fixtures/imgs/mona-lisa.webp",
        "fixtures/imgs/shape.webp",
        "fixtures/imgs/train.webp",
        "fixtures/imgs/KF51.webp",
    ]

    for img in imgs:
        print(img, ss.match(img, labels))
