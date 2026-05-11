from pandas import DataFrame
from impl.Handler import Handler 

class QueryHandler(Handler):
    def getById(self, id: str) -> DataFrame:
        pass