from pandas import DataFrame
from src.base.handler import QueryHandler
import pandas as pd
import requests
import re 

class CitationQueryHandler(QueryHandler):
    def _run_query(self, query: str) -> dict: 
        endpoint = self.getDbPathOrUrl()

        response = requests.get(
            endpoint,
            params={"query": query},
            headers={"Accept": "application/sparql-results+json"}
        )

        response.raise_for_status()
        return response.json()
    
    def _results_to_dataframe(self, results: dict) -> DataFrame: 
        rows = []

        for item in results["results"]["bindings"]:
            row = {}
            for key, value in item.items():
                row[key] = value["value"]
            rows.append(row)

        return pd.DataFrame(rows)
    
    def _duration_to_days(self, duration:str) -> int: 
        pattern = r"P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?" 
        match = re.fullmatch(pattern, duration) 

        if not match:
            return -1
        
        years = int(match.group(1)) if match.group(1) else 0
        months = int(match.group(2)) if match.group(2) else 0
        days = int(match.group(3)) if match.group(3) else 0

        return years * 365 + months * 30 + days 
    
    def _normalize_creation_date(self, creation: str):
        if pd.isna(creation) or creation == "":
            return pd.NaT
        
        creation = str(creation).strip()

        if len(creation) == 4:
            creation = creation + "-01-01"
        elif len(creation) == 7:
            creation = creation + "-01"
        return pd.to_datetime(creation, errors="coerce")
    
    def getById(self, id: str) -> DataFrame:
        citation_uri = f"http://opencitations.net/citation/{id}"

        query = f"""
        SELECT ?citing ?cited ?creation ?timespan ?journal_sc ?author_sc 
        WHERE {{ 
            <{citation_uri}> a <http://purl.org/spar/cito/Citation> ;
                <http://purl.org/spar/cito/hasCitingEntity> ?citing ;
                <http://purl.org/spar/cito/hasCitedEntity> ?cited .
            OPTIONAL {{ <{citation_uri}> <https://schema.org/dateCreated> ?creation . }}
            OPTIONAL {{ <{citation_uri}> <https://schema.org/duration> ?timespan . }}
            OPTIONAL {{ <{citation_uri}> <http://opencitations.net/ontology/journal_sc> ?journal_sc . }}
            OPTIONAL {{ <{citation_uri}> <http://opencitations.net/ontology/author_sc> ?author_sc . }}
        }}
        """

        results = self._run_query(query)
        return self._results_to_dataframe(results)

    def getAllCitations(self) -> DataFrame:
        query = """
        SELECT ?citation ?citing ?cited
        WHERE {
            ?citation a <http://purl.org/spar/cito/Citation> ;
            <http://purl.org/spar/cito/hasCitingEntity> ?citing ;
            <http://purl.org/spar/cito/hasCitedEntity> ?cited .
        }
        """

        results = self._run_query(query)
        return self._results_to_dataframe(results)
        
    def getAllAuthorSelfCitations(self) -> DataFrame:
        query = """
        SELECT ?citation ?citing ?cited ?author_sc
        WHERE {
            ?citation a <http://purl.org/spar/cito/Citation> ;
                <http://purl.org/spar/cito/hasCitingEntity> ?citing ;
                <http://purl.org/spar/cito/hasCitedEntity> ?cited ;
                <http://opencitations.net/ontology/author_sc> ?author_sc .
            FILTER(?author_sc = "yes") 
        }
        """

        results = self._run_query(query)
        return self._results_to_dataframe(results)

    def getAllJournalSelfCitations(self) -> DataFrame:
        query = """
        SELECT ?citation ?citing ?cited ?journal_sc
        WHERE {
            ?citation a <http://purl.org/spar/cito/Citation> ;
                <http://purl.org/spar/cito/hasCitingEntity> ?citing ;
                <http://purl.org/spar/cito/hasCitedEntity> ?cited ;
                <http://opencitations.net/ontology/journal_sc> ?journal_sc .
            FILTER(?journal_sc = "yes")
        }
        """

        results = self._run_query(query)
        return self._results_to_dataframe(results)

    def getCitationsWithinTimespan(self, min_timespan: str, max_timespan: str) -> DataFrame:
        query = """
        SELECT ?citation ?citing ?cited ?timespan 
        WHERE {
            ?citation a <http://purl.org/spar/cito/Citation> ;
                <http://purl.org/spar/cito/hasCitingEntity> ?citing ;
                <http://purl.org/spar/cito/hasCitedEntity> ?cited ;
                <https://schema.org/duration> ?timespan .
        }
        """

        results = self._run_query(query)
        df = self._results_to_dataframe(results)

        min_days = self._duration_to_days(min_timespan)
        max_days = self._duration_to_days(max_timespan)

        df["timespan_days"] = df["timespan"].apply(self._duration_to_days)

        df = df[
            (df["timespan_days"] >= min_days) &
            (df["timespan_days"] <= max_days)
        ]
        
        return df.drop(columns=["timespan_days"])

    def getCitationsWithinDate(self, start_date: str, end_date: str) -> DataFrame:
        query = """
        SELECT ?citation ?citing ?cited ?creation
        WHERE {
            ?citation a <http://purl.org/spar/cito/Citation> ;
                <http://purl.org/spar/cito/hasCitingEntity> ?citing ;
                <http://purl.org/spar/cito/hasCitedEntity> ?cited ;
                <https://schema.org/dateCreated> ?creation .
        }
        """

        results = self._run_query(query)
        df =  self._results_to_dataframe(results)

        df["creation_normalized"] = df["creation"].apply(self._normalize_creation_date)
        
        start_ts = pd.to_datetime(start_date)
        end_ts = pd.to_datetime(end_date)

        df = df[
            (df["creation_normalized"] >= start_ts) &
            (df["creation_normalized"] <= end_ts)
        ]

        return df.drop(columns = ["creation_normalized"]).reset_index(drop=True)