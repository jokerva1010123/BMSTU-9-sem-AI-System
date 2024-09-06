import re
import nltk
nltk.download('punkt')

from commands import *
from rules import *
from prepareData import initPrefer, resetPrefer
from preprocessing import preprocessing, updateSize, updateSex


def _getAnswer():
    while True:
        answer = input().lower()
        if answer == "да":
            return True
        elif answer == "нет":
            return False

        cmdYesNoValidation()


def isAdd():
    cmdAddDefinition()
    return _getAnswer()


def isReset():
    cmdResetDefinition()
    return _getAnswer()


def processDefinition(dictPrefer, dataList):
    flag = 0
    for data in dataList:
        for rule in RULE_ARR:
            regexp = re.compile(rule)
            match = regexp.match(data)
            if match is not None:
                resDict = match.groupdict()
                if rule == NOT_SIMILAR_TO_NAME:
                    dictPrefer["dislikes"].append(resDict["name"])
                elif rule == SIMILAR_TO_NAME:
                    dictPrefer["likes"].append(resDict["name"])
                elif rule == WANT_CATEGORY:
                    dictPrefer["categories"].append(resDict["category"])
                elif rule == WANT_BRAND:
                    dictPrefer["brands"].append(resDict["brand"])
                elif rule == WANT_COLOR:
                    dictPrefer["colors"].append(resDict["color"])
                elif rule == WANT_SIZE_BEFORE or rule == WANT_SIZE_AFTER:
                    dictPrefer["sizes"].append(updateSize(resDict["size"]))
                elif rule == WANT_SEX:
                    dictPrefer["sex"].append(updateSex(resDict["sex"]))
                elif rule == WANT_VERY_LOW_COST:
                    dictPrefer["costliness"].append("Очень низкая стоимость")
                elif rule == WANT_LOW_COST:
                    dictPrefer["costliness"].append("Низкая стоимость")
                elif rule == WANT_AVERAGE_COST:
                    dictPrefer["costliness"].append("Средняя стоимость")
                elif rule == WANT_HIGH_COST:
                    dictPrefer["costliness"].append("Высокая стоимость")
                elif rule == WANT_VERY_HIGH_COST:
                    dictPrefer["costliness"].append("Очень высокая стоимость")
                elif rule == WHAT_EXISTS or rule == SHOW_ANY:
                    pass

                flag = 1
                break

    if flag == 0:
        cmdMissunderstanding()
    
    cmdFind(dictPrefer)


def dialog():
    dictPrefer = initPrefer()
    
    while True:
        cmdDescribe()
        dataProcessed = preprocessing(input())
        processDefinition(dictPrefer, re.split('[,;.!?]', dataProcessed))

        while True:
            if isAdd():
                break
            elif isReset():
                resetPrefer(dictPrefer)
                cmdResetDefinitionComplete()
                break
            else:
                cmdGoodBye()
                return


def main():
    cmdWelcome()
    dialog()


if __name__ == "__main__":
    main()
