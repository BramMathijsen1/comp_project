from __future__ import annotations

from impl.BasicQueryEngine import (
    BasicQueryEngine,
    _parse_timespan,
    _row_to_citation,
    _row_to_author_self_citation,
    _row_to_journal_self_citation,
    _row_to_bib_entity,
)
from impl.AuthorSelfCitation import AuthorSelfCitation
from impl.JournalSelfCitation import JournalSelfCitation
from impl.Citation import Citation


class FullQueryEngine(BasicQueryEngine):
    """
    Extends BasicQueryEngine with four specialised mashup query methods that
    cross-reference the citation database with the bibliographic entity database.
    """

    def getAuthorSelfCitationsByName(self, author_name: str) -> list[AuthorSelfCitation]:
        """
        Return AuthorSelfCitation objects where at least one author matching
        *author_name* (case-insensitive substring of name or surname) is an
        author of BOTH the citing and the cited entity.
        """
        name_lower = author_name.strip().lower()
        bib_map    = self._bib_map()
        results: list[AuthorSelfCitation] = []
        # Delegate to BasicQueryEngine which delegates to handler
        for asc in self.getAllAuthorSelfCitations():
            citing_be = bib_map.get(asc.citing) or bib_map.get(
                "omid:br/" + str(asc.citing).split("/")[-1]
            )
            cited_be = bib_map.get(asc.cited) or bib_map.get(
                "omid:br/" + str(asc.cited).split("/")[-1]
            )

            if citing_be is None or cited_be is None:
                # Flag is set but entities not in relational DB: include as fallback
                results.append(asc)
                continue

            citing_authors = {a.lower() for a in citing_be.getAuthors()}
            cited_authors  = {a.lower() for a in cited_be.getAuthors()}
            common         = citing_authors & cited_authors

            if any(name_lower in auth for auth in common):
                results.append(asc)

        return results

    def getJournalSelfCitationsByName(self, journal_name: str) -> list[JournalSelfCitation]:
        """
        Return JournalSelfCitation objects where the venue of both the citing
        and the cited entity contains *journal_name* (case-insensitive substring)
        and the two venues are the same.
        """
        name_lower = journal_name.strip().lower()
        bib_map    = self._bib_map()
        results: list[JournalSelfCitation] = []

        # Delegate to BasicQueryEngine which delegates to handler
        for jsc in self.getAllJournalSelfCitations():
            citing_be = bib_map.get(jsc.citing) or bib_map.get(
                "omid:br/" + str(jsc.citing).split("/")[-1]
            )
            cited_be = bib_map.get(jsc.cited) or bib_map.get(
                "omid:br/" + str(jsc.cited).split("/")[-1]
            )

            if citing_be is None or cited_be is None:
                results.append(jsc)
                continue

            citing_venue = (citing_be.getVenue() or "").lower()
            cited_venue  = (cited_be.getVenue()  or "").lower()

            if name_lower in citing_venue and citing_venue == cited_venue:
                results.append(jsc)

        return results

    def getCitationsOfBibEntityByTitleWithinDate(
        self,
        bib_entity_title: str,
        min_date: str,
        max_date: str,
    ) -> list[Citation]:
        """
        Return Citation objects where the *cited* entity's title contains
        *bib_entity_title* (case-insensitive) and the creation date falls
        within [min_date, max_date] (ISO date strings, e.g. '2015-01-01').
        """
        title_lower = bib_entity_title.strip().lower()
        bib_map     = self._bib_map()
        results: list[Citation] = []

        # Delegate to BasicQueryEngine which delegates to handler
        for cit in self.getCitationsWithinDate(min_date, max_date):
            cited_be = bib_map.get(cit.cited) or bib_map.get(
                "omid:br/" + str(cit.cited).split("/")[-1]
            )
            if cited_be is None:
                continue

            if title_lower in (cited_be.getTitle() or "").lower():
                results.append(cit)

        return results

    def getReferencesOfBibEntityByTitleWithinTimespan(
        self,
        bib_entity_title: str,
        min_timespan: str,
        max_timespan: str,
    ) -> list[Citation]:
        """
        Return Citation objects where the *citing* entity's title contains
        *bib_entity_title* (case-insensitive) and the citation timespan
        (ISO 8601 duration) falls within [min_timespan, max_timespan].
        """
        title_lower = bib_entity_title.strip().lower()
        bib_map     = self._bib_map()
        results: list[Citation] = []

        # Delegate to BasicQueryEngine which delegates to handler
        for cit in self.getCitationsWithinTimespan(min_timespan, max_timespan):
            citing_be = bib_map.get(cit.citing) or bib_map.get(
                "omid:br/" + str(cit.citing).split("/")[-1]
            )
            if citing_be is None:
                continue

            if title_lower in (citing_be.getTitle() or "").lower():
                results.append(cit)

        return results
