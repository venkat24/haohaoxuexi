from enum import Enum

class CharacterSet(Enum):
    simplified = "simplified"
    traditional = "traditional"

    def __str__(self):
        return self.value

    def getOpposite(self):
        return self.traditional if self.value == self.simplified else self.simplified