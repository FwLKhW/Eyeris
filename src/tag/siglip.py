from libreyolo.models import LibreYOLO


class SigLipTagger:
    model = LibreYOLO("LibreSigLIP2so400m-cls.pt")
    threshold = 0.65

    def set_tags(self, tags: list[str]):
        self.model.set_classes(tags)

    def tag(self, image: str, threshold=threshold) -> list[str]:
        result = self.model(image)
        tags = []
        print([self.model.names[i] for i in result.probs.top5])
        print(result.probs.top5conf)
        for i, conf in enumerate(result.probs.data):
            if conf > threshold:
                tags.append(self.model.names[i])
        return tags


if __name__ == "__main__":
    siglip_tagger = SigLipTagger()
    siglip_tagger.set_tags(["sky", "airplane", "house", "dish"])

    print(siglip_tagger.tag("fixtures/hamburger.jpg"))
