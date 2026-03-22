class IdentifiableEntity:
    def __init__(self):
        self.id: list[str] = []

    def getIds(self) -> list[str]:
        return self.id
