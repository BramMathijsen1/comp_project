from pandas import DataFrame
from src.base.handler import QueryHandler


class CitationQueryHandler(QueryHandler):
    def getById(self, id: str) -> DataFrame:
        pass

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
