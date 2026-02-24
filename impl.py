from pandas import DataFrame
from handler import Handler

class Handler:
    def __init__(self):
        self.dbPathOrUrl: str = ""

    def getDbPathOrUrl(self) -> str:
        pass

    def setDbPathOrUrl(self, pathOrUrl: str) -> bool:
        pass

class UploadHandler(Handler):
    def pushDataToDb(self, path: str) -> bool:
        pass


class QueryHandler(Handler):
    def getById(self, id: str) -> DataFrame:
        pass

class CitationQueryHandler(QueryHandler):
    def getAllCitations(self) -> DataFrame:
        pass

    def getAllAuthorSelfCitations(self) -> DataFrame:
        pass

    def getAllJournalSelfCitations(self) -> DataFrame:
        pass

    def getCitationsWithinTimespan(self, min_timespan: str, max_timespan: str) -> DataFrame:
        pass

    def getCitationsWithinDate(self, start_date: str, end_date: str) -> DataFrame:
        pass


class BibliographicEntityQueryHandler(QueryHandler):
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

class CitationUploadHandler(UploadHandler):
    pass


class BibliographicEntityUploadHandler(UploadHandler):
    pass
