from __future__ import annotations

import pandas as pd

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

    def _concat(self, frames: list) -> pd.DataFrame:
        """Concatenate a list of DataFrames, dropping duplicates."""
        non_empty = [df for df in frames if df is not None and not df.empty]
        if not non_empty:
            return pd.DataFrame()
        return pd.concat(non_empty, ignore_index=True).drop_duplicates()

    def _all_citation_df(self) -> pd.DataFrame:
        """Concatenate getAllCitations() from every registered citation handler."""
        frames = []
        for handler in self.citationQuery:
            try:
                frames.append(handler.getAllCitations())
            except Exception:
                pass
        return self._concat(frames)

    def _all_bib_df(self) -> pd.DataFrame:
        """Concatenate getAllBibliographicEntities() from every registered bib handler."""
        frames = []
        for handler in self.bibliographicEntityQuery:
            try:
                frames.append(handler.getAllBibliographicEntities())
            except Exception:
                pass
        return self._concat(frames)

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
        Delegates to each handler's getById() method.
        """
        # Check bibliographic entity handlers first
        for handler in self.bibliographicEntityQuery:
            try:
                df = handler.getById(id)
                if df is not None and not df.empty:
                    return _row_to_bib_entity(df.iloc[0])
            except Exception:
                pass

        # Then check citation handlers
        for handler in self.citationQuery:
            try:
                df = handler.getById(id)
                if df is not None and not df.empty:
                    return _row_to_citation(df.iloc[0])
            except Exception:
                pass

        return None

    # ── citation queries ───────────────────────────────────────────────────

    def getAllCitations(self) -> list[Citation]:
        return [_row_to_citation(row) for _, row in self._all_citation_df().iterrows()]

    def getAllAuthorSelfCitations(self) -> list[AuthorSelfCitation]:
        """Delegate to each handler's getAllAuthorSelfCitations() and merge."""
        frames = []
        for handler in self.citationQuery:
            try:
                frames.append(handler.getAllAuthorSelfCitations())
            except Exception:
                pass
        df = self._concat(frames)
        return [_row_to_author_self_citation(row) for _, row in df.iterrows()]

    def getAllJournalSelfCitations(self) -> list[JournalSelfCitation]:
        """Delegate to each handler's getAllJournalSelfCitations() and merge."""
        frames = []
        for handler in self.citationQuery:
            try:
                frames.append(handler.getAllJournalSelfCitations())
            except Exception:
                pass
        df = self._concat(frames)
        return [_row_to_journal_self_citation(row) for _, row in df.iterrows()]

    def getCitationsWithinTimespan(self, min_timespan: str, max_timespan: str) -> list[Citation]:
        """Delegate to each handler's getCitationsWithinTimespan() and merge."""
        frames = []
        for handler in self.citationQuery:
            try:
                frames.append(handler.getCitationsWithinTimespan(min_timespan, max_timespan))
            except Exception:
                pass
        df = self._concat(frames)
        return [_row_to_citation(row) for _, row in df.iterrows()]

    def getCitationsWithinDate(self, start_date: str, end_date: str) -> list[Citation]:
        """Delegate to each handler's getCitationsWithinDate() and merge."""
        frames = []
        for handler in self.citationQuery:
            try:
                frames.append(handler.getCitationsWithinDate(start_date, end_date))
            except Exception:
                pass
        df = self._concat(frames)
        return [_row_to_citation(row) for _, row in df.iterrows()]

    # ── bibliographic entity queries ───────────────────────────────────────

    def getAllBibliographicEntities(self) -> list[BibliographicEntity]:
        return [_row_to_bib_entity(row) for _, row in self._all_bib_df().iterrows()]

    def getBibliographicEntitiesWithTitle(self, title: str) -> list[BibliographicEntity]:
        """Delegate to each handler's getBibliographicEntitiesWithTitle() and merge."""
        frames = []
        for handler in self.bibliographicEntityQuery:
            try:
                frames.append(handler.getBibliographicEntitiesWithTitle(title))
            except Exception:
                pass
        df = self._concat(frames)
        return [_row_to_bib_entity(row) for _, row in df.iterrows()]

    def getBibliographicEntitiesWithAuthor(self, author: str) -> list[BibliographicEntity]:
        """Delegate to each handler's getBibliographicEntitiesWithAuthor() and merge."""
        frames = []
        for handler in self.bibliographicEntityQuery:
            try:
                frames.append(handler.getBibliographicEntitiesWithAuthor(author))
            except Exception:
                pass
        df = self._concat(frames)
        return [_row_to_bib_entity(row) for _, row in df.iterrows()]

    def getBibliographicEntitiesWithinDate(self, start_date: str, end_date: str) -> list[BibliographicEntity]:
        """Delegate to each handler's getBibliographicEntitiesWithinPublicationDate() and merge."""
        frames = []
        for handler in self.bibliographicEntityQuery:
            try:
                frames.append(handler.getBibliographicEntitiesWithinPublicationDate(start_date, end_date))
            except Exception:
                pass
        df = self._concat(frames)
        return [_row_to_bib_entity(row) for _, row in df.iterrows()]

    def getBibliographicEntitiesWithVenue(self, venue: str) -> list[BibliographicEntity]:
        """Delegate to each handler's getBibliographicEntitiesWithVenue() and merge."""
        frames = []
        for handler in self.bibliographicEntityQuery:
            try:
                frames.append(handler.getBibliographicEntitiesWithVenue(venue))
            except Exception:
                pass
        df = self._concat(frames)
        return [_row_to_bib_entity(row) for _, row in df.iterrows()]


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
    raw = row.get("authors", row.get("author", ""))
    if not raw:
        return []
    if isinstance(raw, list):
        return [str(a) for a in raw]
    return [s.strip() for s in str(raw).split(";") if s.strip()]


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
