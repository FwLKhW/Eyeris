from pathlib import Path

import platformdirs
from ultralytics import YOLO


class YOLOTagger:
    model = YOLO(platformdirs.user_data_path() / "eyeris" / "yolo26x-cls.pt")
    threshold: float = 0.5
    classes = model.names

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold

    def tag(self, path: Path) -> list[str]:
        results = self.model(path, verbose=False)

        probs = results[0].probs  # ty: ignore[unresolved-attribute, not-subscriptable]
        indexes = probs.top5  # ty: ignore[unresolved-attribute]
        confidences = probs.top5conf  # ty: ignore[unresolved-attribute]

        tags = []
        for i in range(5):
            if confidences[i] > self.threshold:
                tags.append(self.classes[indexes[i]])

        return tags


if __name__ == "__main__":
    yolo_tagger = YOLOTagger()

    print(yolo_tagger.tag(Path("fixtures/hamburger.jpg")))  # ['cheeseburger']
