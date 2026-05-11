import sqlite3
import pandas as pd
from pandas import DataFrame

from impl.QueryHandler import QueryHandler


class BibliographicEntityQueryHandler(QueryHandler):

    def _execute_query(self, query: str, params=None) -> DataFrame:
        if params is None:
            params = []

        with sqlite3.connect(self.getDbPathOrUrl()) as conn:
            df = pd.read_sql_query(query, conn, params=params)

        return df.reset_index(drop=True)

    def _normalize_input_date(self, date_str: str, is_start: bool = True) -> str:
        if len(date_str) == 4:
            return date_str + "-01-01" if is_start else date_str + "-12-31"
        elif len(date_str) == 7:
            return date_str + "-01" if is_start else date_str + "-31"
        return date_str

    def getById(self, id: str) -> DataFrame:
        query = """
        SELECT DISTINCT b.*
        FROM bibliographic_entities b
        LEFT JOIN entity_identifiers e ON b.omid = e.omid
        WHERE b.omid = ?
            OR e.identifier_value = ?
        """
        return self._execute_query(query, [id, id])
    
   

    def getAllBibliographicEntities(self) -> DataFrame:

        query = """
        SELECT DISTINCT *
        FROM bibliographic_entities
        """
        return self._execute_query(query)

    def getBibliographicEntitiesWithTitle(self, title: str) -> DataFrame:

        query = """
        SELECT DISTINCT *
        FROM bibliographic_entities
        WHERE title LIKE ?
        """
        return self._execute_query(query, [f"%{title}%"])

    def getBibliographicEntitiesWithAuthor(self, author: str) -> DataFrame:
       
        query = """
        SELECT DISTINCT b.*
        FROM bibliographic_entities b
        JOIN entity_authors a ON b.omid = a.omid
        WHERE a.author_name LIKE ?
        """
        return self._execute_query(query, [f"%{author}%"])
    
    def getBibliographicEntitiesWithinPublicationDate(self, start_date: str, end_date: str) -> DataFrame:

        normalized_pub_date = """
        CASE
            WHEN length(pub_date) = 4 THEN pub_date || '-01-01'
            WHEN length(pub_date) = 7 THEN pub_date || '-01'
            ELSE pub_date
        END
        """

        query = f"""
        SELECT DISTINCT *
        FROM bibliographic_entities
        WHERE {normalized_pub_date} >= ?
          AND {normalized_pub_date} <= ?
        """

        start_date = self._normalize_input_date(start_date, is_start=True)
        end_date = self._normalize_input_date(end_date, is_start=False)

        return self._execute_query(query, [start_date, end_date])

 

    def getBibliographicEntitiesWithVenue(self, venue: str) -> DataFrame:

        query = """
        SELECT DISTINCT *
        FROM bibliographic_entities
        WHERE venue LIKE ?
        """
        return self._execute_query(query, [f"%{venue}%"])
