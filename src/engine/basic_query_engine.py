from src.models.identifiable_entity import IdentifiableEntity
from src.models.citation import Citation
from src.models.author_self_citation import AuthorSelfCitation
from src.models.journal_self_citation import JournalSelfCitation
from src.models.bibliographic_entity import BibliographicEntity


class BasicQueryEngine:
    def __init__(self):
        self.citationQuery = []
        self.bibliographicEntityQuery = []

    def cleanCitationHandlers(self) -> bool:
        pass

    def cleanBibliographicEntityHandlers(self) -> bool:
        pass

    def addCitationHandler(self, handler) -> bool:
        pass

    def addBibliographicEntityHandler(self, handler) -> bool:
        pass

    def getEntityById(self, id: str) -> IdentifiableEntity | None:
        pass

    def getAllCitations(self) -> list[Citation]:
        pass

    def getAllAuthorSelfCitations(self) -> list[AuthorSelfCitation]:
        pass

    def getAllJournalSelfCitations(self) -> list[JournalSelfCitation]:
        pass

    def getCitationsWithinTimespan(self, min_timespan: str, max_timespan: str) -> list[Citation]:
        pass

    def getCitationsWithinDate(self, start_date: str, end_date: str) -> list[Citation]:
        pass

    def getAllBibliographicEntities(self) -> list[BibliographicEntity]:
        pass

    def getBibliographicEntitiesWithTitle(self, title: str) -> list[BibliographicEntity]:
        pass

    def getBibliographicEntitiesWithAuthor(self, author: str) -> list[BibliographicEntity]:
        pass

    def getBibliographicEntitiesWithinDate(self, start_date: str, end_date: str) -> list[BibliographicEntity]:
        pass

    def getBibliographicEntitiesWithVenue(self, venue: str) -> list[BibliographicEntity]:
        pass
