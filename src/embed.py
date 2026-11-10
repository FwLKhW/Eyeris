from libreyolo.models import LibreYOLO


# Perception Encoder
class PEEmbed:
    model = LibreYOLO("LibrePEt16-cls.pt", task="embed")

    def image(self, image: str):
        result = self.model(image)
        return result.embeddings.data

    def text(self, text: str):
        embed = self.model.embed_text(text)
        return embed


if __name__ == "__main__":
    pe_embed = PEEmbed()

    print(pe_embed.image("fixtures/hamburger.jpg").shape)
    print(pe_embed.text("hamburger").shape)
