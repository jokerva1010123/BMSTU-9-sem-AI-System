import re
import pymorphy3
from nltk.tokenize import word_tokenize


morph = pymorphy3.MorphAnalyzer(lang='ru')


def getNormalFormWord(word):
    return morph.parse(word)[0].normal_form


def delUselessSigns(phrase):
    return re.sub("[^а-яa-z0-9'№ &-,;.!?]", "", phrase)


def getNormalFormPhrase(phrase):
    wordArr = word_tokenize(phrase, language="russian")
    return ' '.join(getNormalFormWord(word) for word in wordArr)


def toLower(phrase: str):
    return phrase.lower()


def preprocessing(phrase: str):
    phrase = toLower(phrase)
    phrase = delUselessSigns(phrase)

    return getNormalFormPhrase(phrase)


def updateSize(size: str):
    sizeDict = { "s": 42, "m": 44, "l": 46, "xl": 48, "xxl": 50 }
    return sizeDict[size] if size in sizeDict else int(size)


def updateSex(sex: str):
    sexDict = { 
        "мужской": 0, 
        "мужчина": 0,
        "парень": 0,
        "женский": 1,
        "женищина": 1,
        "девушка": 1,
    }
    return sexDict[sex]
