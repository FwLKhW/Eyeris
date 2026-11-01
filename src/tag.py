from pathlib import Path

from ultralytics import YOLO


class AutoTagger:
    model = YOLO("yolo26x-cls.pt")
    threshold: float = 0.5
    classes = model.names

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    def tag(self, path: Path) -> list[str]:
        results = self.model(path)

        probs = results[0].probs  # ty: ignore[unresolved-attribute, not-subscriptable]
        indexes = probs.top5  # ty: ignore[unresolved-attribute]
        confidences = probs.top5conf  # ty: ignore[unresolved-attribute]

        tags = []
        for i in range(5):
            if confidences[i] > self.threshold:
                tags.append(self.classes[indexes[i]])

        return tags


if __name__ == "__main__":
    tagger = AutoTagger()

    print(tagger.tag(Path("fixtures/Example/dream.jpg")))
    print(tagger.tag(Path("fixtures/Example/moon.jpg")))
    print(tagger.tag(Path("fixtures/Example/sunset.jpg")))
    print(tagger.tag(Path("fixtures/Example/dinosaur.png")))
