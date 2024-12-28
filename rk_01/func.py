from  preprocessing import *
from measures import *
import pandas as pd
from collections import defaultdict

F_NAME = "Название"
F_DIST = "расстояние"
# Вход: 1 объект (затравочный). 
# Выход: список рекомендаций, ранжированный по убыванию близости с затравкой. Примените Вашу обобщающую меру близости.
def _findSimilar(name, df0, nameArr, matrSimilarity):
    ind = df0[F_NAME].tolist().index(name)
    
    listSimilarity = getSimilarity(ind, matrSimilarity, nameArr)
    return listSimilarity

def findSimilar(name, df0, nameArr, matrSimilarity):
    listSimilarity = _findSimilar(name, df0, nameArr, matrSimilarity)

    return listSimilarity[listSimilarity[F_NAME] != name]

# Вход: массив объектов (лайков). 
# Выход: сформированный ранжированный список рекомендаций.
def _findSimilarMany(Arr, df0, nameArr, matrSimilarity):
    recList = []
    for name in Arr:
        rec = _findSimilar(name, df0, nameArr, matrSimilarity)
        recList.append(rec.loc[rec[F_NAME].isin(Arr) == False])
    dfRes = defaultdict(lambda: 1e2)
    for rec in recList:
        for i, row in rec.iterrows():
            curName = row[F_NAME]
            curDist = row[F_DIST]
            dfRes[curName] = min(dfRes[curName], curDist)

    return dfRes


def findSimilarMany(Arr, df0, nameArr, matrSimilarity):
    resDict = _findSimilarMany(Arr, df0, nameArr, matrSimilarity)
    return sorted([{key: elem} for key, elem in resDict.items()], key=lambda elem: list(elem.values())[0])

# Вход: массив затравочных объектов и массив дизлайков.
# Выход: сформированный ранжированный список рекомендаций.

def delOpposite(dict, nameArr):
    for name in nameArr:
        if name in dict.keys():
            del dict[name]
    
    return dict


def findSimilar3(likesArr, dislikesArr, df0, nameArr, matrSimilarity):
    likesRec = delOpposite(_findSimilarMany(likesArr, df0, nameArr, matrSimilarity), dislikesArr)
    dislikesRec = delOpposite(_findSimilarMany(dislikesArr, df0, nameArr, matrSimilarity), likesArr)

    dictRes = {}
    if len(likesArr) == 0:
        for key, elem in dislikesRec.items():
            if elem > 0.7:
                dictRes[key] = elem
        return sorted([{key: elem} for key, elem in dictRes.items()], key=lambda elem: list(elem.values())[0])

    for key in likesRec.keys():
        if likesRec[key] <= dislikesRec[key]:
            dictRes[key] = likesRec[key]
    return sorted([{key: elem} for key, elem in dictRes.items()], key=lambda elem: list(elem.values())[0])