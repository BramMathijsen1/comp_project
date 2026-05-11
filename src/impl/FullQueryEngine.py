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
        cit_df     = self._all_citation_df()
        bib_map    = self._bib_map()
        results: list[AuthorSelfCitation] = []

        if cit_df.empty:
            return results

        mask   = cit_df["author_sc"].str.strip().str.lower() == "yes"
        asc_df = cit_df[mask]

        for _, row in asc_df.iterrows():
            citing_be = bib_map.get(row["citing"]) or bib_map.get(
                "omid:br/" + str(row["citing"]).split("/")[-1]
            )
            cited_be = bib_map.get(row["cited"]) or bib_map.get(
                "omid:br/" + str(row["cited"]).split("/")[-1]
            )

            if citing_be is None or cited_be is None:
                # Flag is set but entities not in relational DB: include as fallback
                results.append(_row_to_author_self_citation(row))
                continue

            citing_authors = {a.lower() for a in citing_be.getAuthors()}
            cited_authors  = {a.lower() for a in cited_be.getAuthors()}
            common         = citing_authors & cited_authors

            if any(name_lower in auth for auth in common):
                results.append(_row_to_author_self_citation(row))

        return results

    def getJournalSelfCitationsByName(self, journal_name: str) -> list[JournalSelfCitation]:
        """
        Return JournalSelfCitation objects where the venue of both the citing
        and the cited entity contains *journal_name* (case-insensitive substring)
        and the two venues are the same.
        """
        name_lower = journal_name.strip().lower()
        cit_df     = self._all_citation_df()
        bib_map    = self._bib_map()
        results: list[JournalSelfCitation] = []

        if cit_df.empty:
            return results

        mask   = cit_df["journal_sc"].str.strip().str.lower() == "yes"
        jsc_df = cit_df[mask]

        for _, row in jsc_df.iterrows():
            citing_be = bib_map.get(row["citing"]) or bib_map.get(
                "omid:br/" + str(row["citing"]).split("/")[-1]
            )
            cited_be = bib_map.get(row["cited"]) or bib_map.get(
                "omid:br/" + str(row["cited"]).split("/")[-1]
            )

            if citing_be is None or cited_be is None:
                results.append(_row_to_journal_self_citation(row))
                continue

            citing_venue = (citing_be.getVenue() or "").lower()
            cited_venue  = (cited_be.getVenue()  or "").lower()

            if name_lower in citing_venue and citing_venue == cited_venue:
                results.append(_row_to_journal_self_citation(row))

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
        cit_df      = self._all_citation_df()
        bib_map     = self._bib_map()
        results: list[Citation] = []

        if cit_df.empty:
            return results

        for _, row in cit_df.iterrows():
            creation = str(row.get("creation", "")).strip()
            if not creation or not (min_date <= creation <= max_date):
                continue

            cited_be = bib_map.get(row["cited"]) or bib_map.get(
                "omid:br/" + str(row["cited"]).split("/")[-1]
            )
            if cited_be is None:
                continue

            if title_lower in (cited_be.getTitle() or "").lower():
                results.append(_row_to_citation(row))

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
        title_lower  = bib_entity_title.strip().lower()
        min_ts_years = _parse_timespan(min_timespan)
        max_ts_years = _parse_timespan(max_timespan)
        cit_df       = self._all_citation_df()
        bib_map      = self._bib_map()
        results: list[Citation] = []

        if cit_df.empty:
            return results

        for _, row in cit_df.iterrows():
            ts_years = _parse_timespan(str(row.get("timespan", "")))
            if ts_years < 0 or not (min_ts_years <= ts_years <= max_ts_years):
                continue

            citing_be = bib_map.get(row["citing"]) or bib_map.get(
                "omid:br/" + str(row["citing"]).split("/")[-1]
            )
            if citing_be is None:
                continue

            if title_lower in (citing_be.getTitle() or "").lower():
                results.append(_row_to_citation(row))

        return results
