import pinyin

from enum import Enum
from characters import CharacterSet
from hanziconv import HanziConv
from googletrans import Translator

# Represents a card with a simple front and back
class AnkiCard():
    def __init__(self, front, back):
        self.front = front
        self.back = back

    def __str__(self):
        return f'<AnkiCard front={self.front} back={self.back}>'

# Represents a Chinese language flashcard with various fields
class Card():
    @classmethod
    def fields(cls):
        return [
            "content",             # The content of the card, in the standard character set
            "pinyin",              # The pinyin transliteration for the card
            "translation",         # Translation for the card from a translation service
            "definition",          # Definition of the card from a dictionary
            "oppositeCharacters"   # Content in the opposite character set (Simplified <-> Traditional)
        ]

    def __init__(self, characterSet=CharacterSet.simplified, **kwargs):
        self._inputValues = {}
        self._characterSet = characterSet

        # Save each field that has been inputted, the only required field is the content in Chinese
        if "content" not in kwargs.keys():
            print("Each card must have a content field")
            exit(1)

        # Set the input values
        for key, value in kwargs.items():
            if key not in Card.fields():
                print(f"Invalid replacement argument {key} specified.")
                exit(1)

            self._inputValues[key] = value

        # Use the default character set for the content field
        self._inputValues["content"] = self._convertToCharacterSet(self._inputValues["content"], self._characterSet)

    def __str__(self):
        return '<Card' + ",".join(["\n    " + key + ": " + value for key, value in self._inputValues.items() if key != None ]) + ' >'

    def content(self):
        return self._inputValues["content"]
    def pinyin(self):
        return self._inputValues["pinyin"]
    def translation(self):
        return self._inputValues["translation"]
    def definition(self):
        return self._inputValues["definition"]
    def oppositeCharacters(self):
        return self._inputValues["oppositeCharacters"]

    # Given a format string for the front and back of the card, generate the card contents
    def generateAnkiCard(self, frontPattern: str, backPattern: str):
        cardFront = frontPattern
        cardBack = backPattern
        for field in Card.fields():
            pattern = f"{{{field}}}"
            if pattern in cardFront or pattern in cardBack:
                replacement = self._getValue(field)
                cardFront = cardFront.replace(pattern, replacement)
                cardBack = cardBack.replace(pattern, replacement)

        return AnkiCard(cardFront, cardBack)

    # Get the value of the specified field, generating it if necessary
    def _getValue(self, field: str):
        # Some values will be prexisting, and some will be generated
        if field in self._inputValues.keys():
            return self._inputValues[field]

        switcher = {
            "pinyin": self._generatePinyin,
            "translation": self._generateTranslation,
            "definition": self._generateDefinition,
            "oppositeCharacters": self._oppositeCharacterSet
        }

        return switcher[field](self._inputValues["content"])

    # Use the pinyin library to generate accented pinyin
    def _generatePinyin(self, content: str):
        value = pinyin.get(" ".join(list(content)))
        self._inputValues["pinyin"] = value
        return value

    # TODO - Use CC-CEDICT
    def _generateDefinition(self, content: str):
        # TODO
        raise NotImplementedError

    # Generate translation from Google Translate
    def _generateTranslation(self, content: str):
        t = Translator()
        value = t.translate(content).text
        self._inputValues["translation"] = value
        return value

    # Get content in the opposite character set
    def _oppositeCharacterSet(self, content: str):
        value = self._convertToCharacterSet(content, self._characterSet.getOpposite())

        self._inputValues["oppositeCharacters"] = value
        return value

    # Convert to the desired character set
    def _convertToCharacterSet(self, content: str, characterSet: CharacterSet):
        if characterSet == CharacterSet.simplified:
            value = HanziConv.toSimplified(content)
        else:
            value = HanziConv.toTraditional(content)
        return value