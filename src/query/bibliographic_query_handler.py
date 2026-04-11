import sqlite3
import pandas as pd
from pandas import DataFrame
from src.base.handler import QueryHandler


class BibliographicEntityQueryHandler(QueryHandler):
    def getById(self, id: str) -> DataFrame:

        conn = sqlite3.connect(self.getDbPathOrUrl())
        query = """
        SELECT DISTINCT b.*
        FROM bibliographic_entities b
        LEFT JOIN entity_identifiers e ON b.omid = e.omid
        WHERE (e.identifier_value = ?
        OR b.omid = ?)
        """

        df = pd.read_sql_query(query, conn, params=[id, id])
        conn.close()

        return df.reset_index(drop=True)
    
   

    def getAllBibliographicEntities(self) -> DataFrame:

        conn = sqlite3.connect(self.getDbPathOrUrl())

        query = """
        SELECT *
        FROM bibliographic_entities
        """

        df = pd.read_sql_query(query, conn)
        conn.close()

        return df.reset_index(drop=True)

    def getBibliographicEntitiesWithTitle(self, title: str) -> DataFrame:

        conn = sqlite3.connect(self.getDbPathOrUrl())

        query = """
        SELECT *
        FROM bibliographic_entities
        WHERE title LIKE ?
        """

        df = pd.read_sql_query(query, conn, params=[f"%{title}%"])  
        conn.close()

        return df.reset_index(drop=True)

    def getBibliographicEntitiesWithAuthor(self, author: str) -> DataFrame:
       
        conn = sqlite3.connect(self.getDbPathOrUrl())

        query = """
        SELECT DISTINCT b.*
        FROM bibliographic_entities b
        JOIN entity_authors a ON b.omid = a.omid
        WHERE a.author_name LIKE ?
        """

        df = pd.read_sql_query(query, conn, params=[f"%{author}%"])
        conn.close()

        return df.reset_index(drop=True)

    def getBibliographicEntitiesWithinPublicationDate(self, start_date: str, end_date: str) -> DataFrame:
        def normalize_input_date(date_str: str, is_start=True):
            if len(date_str) == 4:
                return date_str + "-01-01" if is_start else date_str + "-12-31"
            elif len(date_str) == 7:
                return date_str + "-01" if is_start else date_str + "-31"
            return date_str

        conn = sqlite3.connect(self.getDbPathOrUrl())

        query = """
        SELECT *
        FROM bibliographic_entities
        WHERE 1=1
        """

        params = []

        normalized_pub_date = """
        CASE
            WHEN length(pub_date) = 4 THEN pub_date || '-01-01'
            WHEN length(pub_date) = 7 THEN pub_date || '-01'
            ELSE pub_date
        END
        """

        if start_date:
            start_date = normalize_input_date(start_date, is_start=True)
            query += f" AND {normalized_pub_date} >= ?"
            params.append(start_date)

        if end_date:
            end_date = normalize_input_date(end_date, is_start=False)
            query += f" AND {normalized_pub_date} <= ?"
            params.append(end_date)

        df = pd.read_sql_query(query, conn, params=params)
        conn.close()

        return df.reset_index(drop=True)
    
        def normalize_input_date(date_str: str, is_start=True):
            if len(date_str) == 4:
                return date_str + "-01-01" if is_start else date_str + "-12-31"
            elif len(date_str) == 7:
                return date_str + "-01" if is_start else date_str + "-31"
            return date_str

    def getBibliographicEntitiesWithVenue(self, venue: str) -> DataFrame:

        conn = sqlite3.connect(self.getDbPathOrUrl())

        query = """
        SELECT *
        FROM bibliographic_entities
        WHERE venue LIKE ?
        """

        df = pd.read_sql_query(query, conn, params=[f"%{venue}%"])
        conn.close()

        return df.reset_index(drop=True)
