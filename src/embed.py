from libreyolo.models import LibreYOLO


# Perception Encoder
class PEEmbed:
    model = LibreYOLO("LibrePEl14-cls.pt", task="embed")

    def image(self, image: str):
        result = self.model(image)
        return result.embeddings.data.squeeze(0)

    def text(self, text: str):
        embed = self.model.embed_text(text)
        return embed.squeeze(0)


if __name__ == "__main__":
    pe_embed = PEEmbed()

    print(pe_embed.image("fixtures/hamburger.jpg").shape)
    print(pe_embed.text("hamburger").shape)
