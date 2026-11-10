from libreyolo.models import LibreYOLO


class SigLipTagger:
    model = LibreYOLO("LibreSigLIP2b16-cls.pt")
    threshold = 0.65

    def set_tags(self, tags: list[str]):
        self.model.set_classes(tags, multi_label=True)

    def tag(self, image: str, threshold=threshold) -> list[str]:
        result = self.model(image)
        tags = []
        for i, conf in enumerate(result.probs.data):
            if conf > threshold:
                tags.append(self.model.names[i])
        return tags


if __name__ == "__main__":
    siglip_tagger = SigLipTagger()
    # siglip_tagger.set_tags(["sky", "airplane", "house", "dish"])

    print(siglip_tagger.tag("fixtures/hamburger.jpg"))
