from pandas import DataFrame

class Handler:
    def __init__(self):
        self.dbPathOrUrl: str = ""

    def getDbPathOrUrl(self) -> str:
        pass

    def setDbPathOrUrl(self, pathOrUrl: str) -> bool:
        pass

class UploadHandler(Handler):
    def pushDataToDb(self, path: str) -> bool:
        pass


class QueryHandler(Handler):
    def getById(self, id: str) -> DataFrame:
        pass