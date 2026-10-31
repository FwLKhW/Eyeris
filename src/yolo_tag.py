from pathlib import Path

from ultralytics import YOLO


class AutoTagger:
    model = YOLO("yolo26x-cls.pt")
    thres = 0.5
    classes = model.names

    def tag(self, path: Path) -> list[str]:
        results = self.model(path)

        idxs = results[0].probs.top5
        confs = results[0].probs.top5conf

        tags = []
        for i in range(5):
            if confs[i] > self.thres:
                tags.append(self.classes[idxs[i]])

        return tags


if __name__ == "__main__":
    tagger = AutoTagger()

    print(tagger.tag(Path("fixtures/imgs/fighters.jpg")))
    print(tagger.tag(Path("fixtures/imgs/mona-lisa.webp")))
    print(tagger.tag(Path("fixtures/imgs/shape.webp")))
    print(tagger.tag(Path("fixtures/imgs/train.webp")))
    print(tagger.tag(Path("fixtures/imgs/KF51.webp")))
