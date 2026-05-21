from impl.identifiable_entity import IdentifiableEntity
from impl.BibliographicEntity import BibliographicEntity

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

    def __repr__(self):
        return (f"Citation(oci={self.oci!r}, citing={self.citing!r}, "
                f"cited={self.cited!r}, creation={self.creation!r}, "
                f"timespan={self.timespan!r}, journal_sc={self.journal_sc!r}, "
                f"author_sc={self.author_sc!r})")

    def getCreation(self) -> str:
        pass

    def getTimespan(self) -> str:
        pass

    def getCitingEntity(self) -> BibliographicEntity:
        pass

    def getCitedEntity(self) -> BibliographicEntity:
        pass
