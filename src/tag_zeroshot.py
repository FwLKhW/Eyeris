from libreyolo.models import LibreYOLO


# Perception Encoder
class PETagger:
    model = LibreYOLO("LibrePEt16-cls.pt")
    threshold = 0.65

    def set_tags(self, tags: list[str]):
        self.model.set_classes(tags)

    def tag(self, image: str, threshold=threshold) -> list[str]:
        result = self.model(image)
        tags = []
        for i, conf in enumerate(result.probs.data):
            if conf > threshold:
                tags.append(self.model.names[i])
        return tags


if __name__ == "__main__":
    pe_tagger = PETagger()
    pe_tagger.set_tags(["burger", "sausage", "banh_mi", "noddle"])

    print(pe_tagger.tag("fixtures/hamburger.jpg"))
