from libreyolo.models import LibreYOLO


# Perception Encoder
class PETagger:
    model = LibreYOLO("LibrePEl14-cls.pt")
    threshold = 0.65

    def set_tags(self, tags: list[str]):
        self.model.set_classes(tags)

    def tag(self, image: str, threshold=threshold) -> str | None:
        result = self.model(image)
        if result.probs.top1conf > threshold:
            return self.model.names[result.probs.top1]
        return None


if __name__ == "__main__":
    pe_tagger = PETagger()
    # pe_tagger.set_tags(["burger", "sausage", "banh_mi", "fried potato"])  # burger
    pe_tagger.set_tags(["sky", "airplane", "house", "dish"])  # dish

    print(pe_tagger.tag("fixtures/hamburger.jpg"))
