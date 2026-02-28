import pandas as pd
import requests  
from src.base.handler import UploadHandler


class CitationUploadHandler(UploadHandler):

    def pushDataToDb(self, path: str) -> bool:
        try:
            df = pd.read_csv(path)
            endpoint = self.getDbPathOrUrl()

            all_triples = ""

            for index, row in df.iterrows():
                triples = f"<http://opencitations.net/citation/{row['oci']}> a <http://purl.org/spar/cito/Citation> ;"
                triples += f'    <http://purl.org/spar/cito/hasCitingEntity> <{row["citing"]}> ;'
                triples += f'    <http://purl.org/spar/cito/hasCitedEntity> <{row["cited"]}> ;'

                if pd.notna(row['creation']) and row['creation'] != "":
                    triples += f'    <https://schema.org/dateCreated> "{row["creation"]}" ;'

                if pd.notna(row['timespan']) and row['timespan'] != "":
                    triples += f'    <https://schema.org/duration> "{row["timespan"]}" ;'

                if pd.notna(row['journal_sc']) and row['journal_sc'] != "":
                    triples += f'    <http://opencitations.net/ontology/journal_sc> "{row["journal_sc"]}" ;'

                if pd.notna(row['author_sc']) and row['author_sc'] != "":
                    triples += f'    <http://opencitations.net/ontology/author_sc> "{row["author_sc"]}" ;'

                triples = triples.rstrip(";")
                triples = triples + " ."
                all_triples += triples

            sparql = f"INSERT DATA {{\n{all_triples}}}"

            response = requests.post(
                endpoint,
                data={"update": sparql},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )

            if not response.ok:
                print(f"Failed, status: {response.status_code}, reason: {response.text}")
                return False

            return True
        except Exception as e:
            print(f"Error: {e}")
            return False