from src.models.identifiable_entity import IdentifiableEntity


class BibliographicEntity(IdentifiableEntity):
    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.author: list[str] = []
        self.publication_date: str = ""
        self.venue: str = ""

    def getTitle(self) -> str:
        pass

    def getAuthors(self) -> list[str]:
        pass

    def getPublicationDate(self) -> str:
        pass

    def getVenue(self) -> str:
        pass
