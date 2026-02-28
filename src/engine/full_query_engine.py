from src.engine.basic_query_engine import BasicQueryEngine
from src.models.author_self_citation import AuthorSelfCitation
from src.models.journal_self_citation import JournalSelfCitation
from src.models.citation import Citation


class FullQueryEngine(BasicQueryEngine):
    def getAuthorSelfCitationsByName(self, author_name: str) -> list[AuthorSelfCitation]:
        pass

    def getJournalSelfCitationsByName(self, journal_name: str) -> list[JournalSelfCitation]:
        pass

    def getCitationsOfBibEntityByTitleWithinDate(
        self,
        bib_entity_title: str,
        min_date: str,
        max_date: str
    ) -> list[Citation]:
        pass

    def getReferencesOfBibEntityByTitleWithinTimespan(
        self,
        bib_entity_title: str,
        min_timespan: str,
        max_timespan: str
    ) -> list[Citation]:
        pass
