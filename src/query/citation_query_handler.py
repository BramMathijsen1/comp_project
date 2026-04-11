from pandas import DataFrame
from src.base.handler import QueryHandler


class CitationQueryHandler(QueryHandler):
    def getById(self, id: str) -> DataFrame:
        import pandas as pd

        df = pd.read_csv(self.getDbPathOrUrl())

        return df[df["oci"] == id]

    def getAllCitations(self) -> DataFrame:
        import pandas as pd
        return pd.read_csv(self.getDbPathOrUrl())

    def getAllAuthorSelfCitations(self) -> DataFrame:
        import pandas as pd
        df = pd.read_csv(self.getDbPathOrUrl())

        return df[df["author_sc"] == "yes"]

    def getAllJournalSelfCitations(self) -> DataFrame:
        import pandas as pd

        df = pd.read_csv(self.getDbPathOrUrl())

        return df[df["journal_sc"] == "yes"]

    def getCitationsWithinTimespan(self, min_timespan: str, max_timespan: str) -> DataFrame:
        import pandas as pd
        import re

        df = pd.read_csv(self.getDbPathOrUrl())

        def duration_to_days(duration: str) -> int:
            if pd.isna(duration) or duration == "":
                return 0

            match = re.fullmatch(r"P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)D)?", duration)
            if not match:
                return 0

            years = int(match.group(1)) if match.group(1) else 0
            months = int(match.group(2)) if match.group(2) else 0
            days = int(match.group(3)) if match.group(3) else 0

            return years * 365 + months * 30 + days

        df["timespan_days"] = df["timespan"].apply(duration_to_days)

        min_days = duration_to_days(min_timespan) if min_timespan else None
        max_days = duration_to_days(max_timespan) if max_timespan else None

        if min_days is not None:
            df = df[df["timespan_days"] >= min_days]

        if max_days is not None:
            df = df[df["timespan_days"] <= max_days]

        return df.drop(columns=["timespan_days"])

    def getCitationsWithinDate(self, start_date: str, end_date: str) -> DataFrame:
        import pandas as pd

        df = pd.read_csv(self.getDbPathOrUrl())

        df["creation"] = pd.to_datetime(df["creation"], format="mixed", errors="coerce")

        if start_date:
            start_date = pd.to_datetime(start_date)
            df = df[df["creation"] >= start_date]

        if end_date:
            end_date = pd.to_datetime(end_date)
            df = df[df["creation"] <= end_date]

        return df.reset_index(drop=True)
