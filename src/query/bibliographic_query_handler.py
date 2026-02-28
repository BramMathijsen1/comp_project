from pandas import DataFrame
from src.base.handler import QueryHandler


class BibliographicEntityQueryHandler(QueryHandler):
    def getById(self, id: str) -> DataFrame:
        pass

    def getAllBibliographicEntities(self) -> DataFrame:
        pass

    def getBibliographicEntitiesWithTitle(self, title: str) -> DataFrame:
        pass

    def getBibliographicEntitiesWithAuthor(self, author: str) -> DataFrame:
        pass

    def getBibliographicEntitiesWithinPublicationDate(self, start_date: str, end_date: str) -> DataFrame:
        pass

    def getBibliographicEntitiesWithVenue(self, venue: str) -> DataFrame:
        pass
