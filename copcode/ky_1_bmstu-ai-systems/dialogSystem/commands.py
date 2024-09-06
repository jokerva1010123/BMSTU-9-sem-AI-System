from data import df0, nameArr
from params import *
from prepareData import find


def cmdOffer():
    print(DEFAULT_DATA)


def cmdWelcome():
    print(WELCOME_PHRASE)


def cmdGoodBye():
    print(GOODBYE_PHRASE)


def cmdDescribe():
    print(DESCRIBE)


def cmdYesNoValidation():
    print(YES_NO)


def cmdAddDefinition():
    print(ADD_DEFINITION)


def cmdResetDefinition():
    print(RESET_PHRASE)


def cmdResetDefinitionComplete():
    print(RESET_PHRASE_COMPLETE)


def cmdMissunderstanding():
    print(MISUNDERSTANDING)


def cmdGiveMustRecomendation():
    print(MUST_LIKE)


def cmdGiveMayRecomendation():
    print(MAY_LIKE)


def _printRecomendations(recArr):
    iArr = []
    n = min(len(recArr), 5)
    for i in range(n):
        iArr.append(df0.index[df0["Название"] == recArr[i]].tolist()[0])

    print(df0.loc[iArr, ["Название", "Пол", "Цвет", "Цена", "Размер", "Бренд"]])


def cmdFind(dictPrefer):
    recMust, recMaybe = find(dictPrefer)

    if len(recMust):
        cmdGiveMustRecomendation()
        _printRecomendations(recMust)

    if len(recMaybe):
        cmdGiveMayRecomendation()
        _printRecomendations(recMaybe)

    if len(recMust) == 0 and len(recMaybe) == 0:
        cmdOffer()
        _printRecomendations(nameArr)
