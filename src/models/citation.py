from src.models.identifiable_entity import IdentifiableEntity
from src.models.bibliographic_entity import BibliographicEntity

class Citation(IdentifiableEntity):
    def __init__(self):
        super().__init__()
        self.oci: str = ""
        self.citing: str = ""
        self.cited: str = ""
        self.creation: str = ""
        self.timespan: str = ""
        self.journal_sc: str = ""
        self.author_sc: str = ""

    def getCreation(self) -> str:
        pass

    def getTimespan(self) -> str:
        pass

    def getCitingEntity(self) -> BibliographicEntity:
        pass

    def getCitedEntity(self) -> BibliographicEntity:
        pass
