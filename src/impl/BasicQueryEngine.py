from __future__ import annotations

from impl.identifiable_entity import IdentifiableEntity
from impl.Citation import Citation
from impl.AuthorSelfCitation import AuthorSelfCitation
from impl.JournalSelfCitation import JournalSelfCitation
from impl.BibliographicEntity import BibliographicEntity


class BasicQueryEngine:
    def __init__(self):
        self.citationQuery = []
        self.bibliographicEntityQuery = []

    # ── handler registration ───────────────────────────────────────────────

    def cleanCitationHandlers(self) -> bool:
        self.citationQuery = []
        return True

    def cleanBibliographicEntityHandlers(self) -> bool:
        self.bibliographicEntityQuery = []
        return True

    def addCitationHandler(self, handler) -> bool:
        if handler not in self.citationQuery:
            self.citationQuery.append(handler)
        return True

    def addBibliographicEntityHandler(self, handler) -> bool:
        if handler not in self.bibliographicEntityQuery:
            self.bibliographicEntityQuery.append(handler)
        return True

    # ── internal DataFrame helpers ─────────────────────────────────────────

    def _all_citation_df(self):
        """Concatenate DataFrames from all registered citation handlers."""
        import pandas as pd
        frames = []
        for handler in self.citationQuery:
            try:
                df = handler.getAllCitations()
                if df is not None and not df.empty:
                    frames.append(df)
            except Exception:
                pass
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    def _all_bib_df(self):
        """Concatenate DataFrames from all registered bib-entity handlers."""
        import pandas as pd
        frames = []
        for handler in self.bibliographicEntityQuery:
            try:
                df = handler.getAllEntities()
                if df is not None and not df.empty:
                    frames.append(df)
            except Exception:
                pass
        return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()

    def _bib_map(self) -> dict[str, BibliographicEntity]:
        """Return {omid: BibliographicEntity} for fast lookup."""
        result: dict[str, BibliographicEntity] = {}
        for _, row in self._all_bib_df().iterrows():
            be = _row_to_bib_entity(row)
            result[str(row["omid"])] = be
        return result

    # ── entity lookup ──────────────────────────────────────────────────────

    def getEntityById(self, id: str) -> IdentifiableEntity | None:
        """
        Search both databases for an entity whose identifier list contains
        *id*. Returns the first match as a domain object, or None.
        """
        # Check bibliographic entities first
        bib_df = self._all_bib_df()
        if not bib_df.empty:
            for _, row in bib_df.iterrows():
                ids = _parse_ids(row)
                if id in ids or str(row.get("omid", "")) == id:
                    return _row_to_bib_entity(row)

        # Then check citations
        cit_df = self._all_citation_df()
        if not cit_df.empty:
            for _, row in cit_df.iterrows():
                if str(row.get("citation", "")) == id:
                    return _row_to_citation(row)

        return None

    # ── citation queries ───────────────────────────────────────────────────

    def getAllCitations(self) -> list[Citation]:
        return [_row_to_citation(row) for _, row in self._all_citation_df().iterrows()]

    def getAllAuthorSelfCitations(self) -> list[AuthorSelfCitation]:
        df = self._all_citation_df()
        if df.empty:
            return []
        mask = df["author_sc"].str.strip().str.lower() == "yes"
        return [_row_to_author_self_citation(row) for _, row in df[mask].iterrows()]

    def getAllJournalSelfCitations(self) -> list[JournalSelfCitation]:
        df = self._all_citation_df()
        if df.empty:
            return []
        mask = df["journal_sc"].str.strip().str.lower() == "yes"
        return [_row_to_journal_self_citation(row) for _, row in df[mask].iterrows()]

    def getCitationsWithinTimespan(self, min_timespan: str, max_timespan: str) -> list[Citation]:
        """Return citations whose timespan falls within [min_timespan, max_timespan] (ISO 8601)."""
        min_y = _parse_timespan(min_timespan)
        max_y = _parse_timespan(max_timespan)
        results: list[Citation] = []
        for _, row in self._all_citation_df().iterrows():
            ts_y = _parse_timespan(str(row.get("timespan", "")))
            if ts_y >= 0 and min_y <= ts_y <= max_y:
                results.append(_row_to_citation(row))
        return results

    def getCitationsWithinDate(self, start_date: str, end_date: str) -> list[Citation]:
        """Return citations whose creation date falls within [start_date, end_date]."""
        results: list[Citation] = []
        for _, row in self._all_citation_df().iterrows():
            creation = str(row.get("creation", "")).strip()
            if creation and start_date <= creation <= end_date:
                results.append(_row_to_citation(row))
        return results

    # ── bibliographic entity queries ───────────────────────────────────────

    def getAllBibliographicEntities(self) -> list[BibliographicEntity]:
        return [_row_to_bib_entity(row) for _, row in self._all_bib_df().iterrows()]

    def getBibliographicEntitiesWithTitle(self, title: str) -> list[BibliographicEntity]:
        title_lower = title.strip().lower()
        return [
            _row_to_bib_entity(row)
            for _, row in self._all_bib_df().iterrows()
            if title_lower in str(row.get("title", "")).lower()
        ]

    def getBibliographicEntitiesWithAuthor(self, author: str) -> list[BibliographicEntity]:
        author_lower = author.strip().lower()
        results: list[BibliographicEntity] = []
        for _, row in self._all_bib_df().iterrows():
            authors = _parse_author_list(row)
            if any(author_lower in a.lower() for a in authors):
                results.append(_row_to_bib_entity(row))
        return results

    def getBibliographicEntitiesWithinDate(self, start_date: str, end_date: str) -> list[BibliographicEntity]:
        results: list[BibliographicEntity] = []
        for _, row in self._all_bib_df().iterrows():
            pub_date = str(row.get("pub_date", "")).strip()
            if pub_date and start_date <= pub_date <= end_date:
                results.append(_row_to_bib_entity(row))
        return results

    def getBibliographicEntitiesWithVenue(self, venue: str) -> list[BibliographicEntity]:
        venue_lower = venue.strip().lower()
        return [
            _row_to_bib_entity(row)
            for _, row in self._all_bib_df().iterrows()
            if venue_lower in str(row.get("venue", "")).lower()
        ]


# ──────────────────────────────────────────────────────────────────────────────
# shared helpers (used by both BasicQueryEngine and FullQueryEngine)
# ──────────────────────────────────────────────────────────────────────────────

def _parse_timespan(ts: str) -> float:
    """
    Convert an ISO 8601 duration string (e.g. 'P2Y6M15D') to fractional years.
    Returns -1.0 for empty / unparseable input.
    """
    if not ts:
        return -1.0
    ts = ts.strip()
    if not ts.startswith("P"):
        return -1.0
    try:
        import re
        years  = float(re.search(r"(\d+(?:\.\d+)?)Y", ts).group(1)) if re.search(r"\d+Y", ts) else 0.0
        months = float(re.search(r"(\d+(?:\.\d+)?)M", ts).group(1)) if re.search(r"\d+M", ts) else 0.0
        days   = float(re.search(r"(\d+(?:\.\d+)?)D", ts).group(1)) if re.search(r"\d+D", ts) else 0.0
        return years + months / 12.0 + days / 365.0
    except Exception:
        return -1.0


def _parse_ids(row) -> list[str]:
    """Return a list of identifier strings for a bib-entity row."""
    raw = row.get("ids", row.get("id", ""))
    if not raw:
        return []
    if isinstance(raw, list):
        return [str(i) for i in raw]
    return [s.strip() for s in str(raw).split(",") if s.strip()]


def _parse_author_list(row) -> list[str]:
    """Return the list of author name strings for a bib-entity row."""
    raw = row.get("authors", row.get("author", ""))
    if not raw:
        return []
    if isinstance(raw, list):
        return [str(a) for a in raw]
    return [s.strip() for s in str(raw).split(",") if s.strip()]


def _extract_oci(uri: str) -> str:
    """Strip the URI prefix to recover the bare oci string."""
    return uri.split("/")[-1]


def _row_to_citation(row) -> Citation:
    c = Citation()
    c.oci        = _extract_oci(str(row["citation"]))
    c.id         = [c.oci]
    c.citing     = str(row["citing"])
    c.cited      = str(row["cited"])
    c.creation   = str(row.get("creation", ""))
    c.timespan   = str(row.get("timespan", ""))
    c.journal_sc = str(row.get("journal_sc", ""))
    c.author_sc  = str(row.get("author_sc", ""))
    return c


def _row_to_author_self_citation(row) -> AuthorSelfCitation:
    asc = AuthorSelfCitation()
    asc.oci        = _extract_oci(str(row["citation"]))
    asc.id         = [asc.oci]
    asc.citing     = str(row["citing"])
    asc.cited      = str(row["cited"])
    asc.creation   = str(row.get("creation", ""))
    asc.timespan   = str(row.get("timespan", ""))
    asc.journal_sc = str(row.get("journal_sc", ""))
    asc.author_sc  = str(row.get("author_sc", ""))
    return asc


def _row_to_journal_self_citation(row) -> JournalSelfCitation:
    jsc = JournalSelfCitation()
    jsc.oci        = _extract_oci(str(row["citation"]))
    jsc.id         = [jsc.oci]
    jsc.citing     = str(row["citing"])
    jsc.cited      = str(row["cited"])
    jsc.creation   = str(row.get("creation", ""))
    jsc.timespan   = str(row.get("timespan", ""))
    jsc.journal_sc = str(row.get("journal_sc", ""))
    jsc.author_sc  = str(row.get("author_sc", ""))
    return jsc


def _row_to_bib_entity(row) -> BibliographicEntity:
    be = BibliographicEntity()
    be.id               = [str(row["omid"])]
    be.title            = str(row.get("title", ""))
    be.publication_date = str(row.get("pub_date", ""))
    be.venue            = str(row.get("venue", ""))
    be.author           = _parse_author_list(row)
    return be