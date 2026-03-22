from src.models.identifiable_entity import IdentifiableEntity


class BibliographicEntity(IdentifiableEntity):
    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.author: list[str] = []
        self.publication_date: str = ""
        self.venue: str = ""

    def getTitle(self) -> str:
        return self.title

    def getAuthors(self) -> list[str]:
        return self.author

    def getPublicationDate(self) -> str:
        return self.publication_date

    def getVenue(self) -> str:
        return self.venue
