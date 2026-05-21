# -*- coding: utf-8 -*-
import unittest
from os import sep
from impl import CitationQueryHandler, BibliographicEntityQueryHandler
from impl import FullQueryEngine
from impl import Citation, AuthorSelfCitation, JournalSelfCitation
from config import grp_endpoint


class TestFullQueryEngine(unittest.TestCase):

    citation   = "data" + sep + "dh_citations.csv"
    bib_entity = "data" + sep + "dh_metadata.json"
    relational = "." + sep + "relational.db"
    graph      = grp_endpoint

    @classmethod
    def setUpClass(cls):
        jq = CitationQueryHandler()
        jq.setDbPathOrUrl(cls.graph)

        cq = BibliographicEntityQueryHandler()
        cq.setDbPathOrUrl(cls.relational)

        cls.fq = FullQueryEngine()
        cls.fq.addCitationHandler(jq)
        cls.fq.addBibliographicEntityHandler(cq)

    # ── getAuthorSelfCitationsByName ───────────────────────────────────────

    def test_01_getAuthorSelfCitationsByName_terras(self):
        """Terras, Melissa has exactly 5 author self-citations in the dataset."""
        r = self.fq.getAuthorSelfCitationsByName("Terras")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, AuthorSelfCitation)

        expected_ocis = {
            "061701739073-061701739087",
            "062202487256-06802923645",
            "062202487256-061101881624",
            "062304256330-06801162133",
            "06802923645-061501794750",
        }
        returned_ocis = {i.oci for i in r}
        self.assertEqual(returned_ocis, expected_ocis)

    def test_02_getAuthorSelfCitationsByName_warwick(self):
        """Warwick, Claire has exactly 6 author self-citations in the dataset."""
        r = self.fq.getAuthorSelfCitationsByName("Warwick")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, AuthorSelfCitation)
        self.assertEqual(len(r), 6)

    def test_03_getAuthorSelfCitationsByName_no_results(self):
        """'Matt' does not appear as an author in any self-citation pair."""
        r = self.fq.getAuthorSelfCitationsByName("Matt")
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 0)

    # ── getJournalSelfCitationsByName ──────────────────────────────────────

    def test_04_getJournalSelfCitationsByName_dsh(self):
        """Digital Scholarship in the Humanities has 38 journal self-citations."""
        r = self.fq.getJournalSelfCitationsByName("Digital Scholarship in the Humanities")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, JournalSelfCitation)
        self.assertEqual(len(r), 38)

    def test_05_getJournalSelfCitationsByName_journal_of_documentation(self):
        """Journal of Documentation has 44 journal self-citations."""
        r = self.fq.getJournalSelfCitationsByName("Journal of Documentation")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, JournalSelfCitation)
        self.assertEqual(len(r), 44)

    def test_06_getJournalSelfCitationsByName_no_results(self):
        """A non-existent journal name returns an empty list."""
        r = self.fq.getJournalSelfCitationsByName("This Journal Does Not Exist")
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 0)

    # ── getCitationsOfBibEntityByTitleWithinDate ───────────────────────────

    def test_07_getCitationsOfBibEntityByTitleWithinDate(self):
        """Citations of entities with 'digital' in title, created 2015-2020."""
        r = self.fq.getCitationsOfBibEntityByTitleWithinDate("digital", "2015", "2020")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Citation)
        self.assertEqual(len(r), 898)

    def test_08_getCitationsOfBibEntityByTitleWithinDate_specific_oci(self):
        """A known OCI is present in the results."""
        r = self.fq.getCitationsOfBibEntityByTitleWithinDate("digital", "2015", "2020")
        returned_ocis = {i.oci for i in r}
        self.assertIn("0610112773-062101784831", returned_ocis)

    def test_09_getCitationsOfBibEntityByTitleWithinDate_no_results(self):
        """A title that doesn't exist returns an empty list."""
        r = self.fq.getCitationsOfBibEntityByTitleWithinDate("zzznomatch", "2015", "2020")
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 0)

    # ── getReferencesOfBibEntityByTitleWithinTimespan ──────────────────────

    def test_10_getReferencesOfBibEntityByTitleWithinTimespan(self):
        """References from entities with 'digital' in title, timespan P2Y-P15Y."""
        r = self.fq.getReferencesOfBibEntityByTitleWithinTimespan("digital", "P2Y", "P15Y")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Citation)
        self.assertEqual(len(r), 8329)

    def test_11_getReferencesOfBibEntityByTitleWithinTimespan_specific_oci(self):
        """A known OCI is present in the results."""
        r = self.fq.getReferencesOfBibEntityByTitleWithinTimespan("digital", "P2Y", "P15Y")
        returned_ocis = {i.oci for i in r}
        self.assertIn("0604904485-06101696600", returned_ocis)

    def test_12_getReferencesOfBibEntityByTitleWithinTimespan_no_results(self):
        """A title that doesn't exist returns an empty list."""
        r = self.fq.getReferencesOfBibEntityByTitleWithinTimespan("zzznomatch", "P2Y", "P15Y")
        self.assertIsInstance(r, list)
        self.assertEqual(len(r), 0)


if __name__ == "__main__":
    unittest.main()
