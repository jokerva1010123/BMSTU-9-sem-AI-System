import pandas as pd
import numpy as np
import itertools
from collections import defaultdict
import math
from cmath import isnan, nan
from numpy import dot
from numpy.linalg import norm

pd.set_option('display.max_columns', None)
df0 = pd.read_csv('data.csv', delimiter=',', encoding="utf8")
df = df0.copy(deep=True)

# ----------------------------------------------------------
smellLike = pd.read_csv('smells.csv', delimiter=',', encoding="utf8")

smellLike["семейство"] = smellLike["семейство"].map(lambda elem: str(elem).lower())
smellLike["ассоциации"] = smellLike["ассоциации"].map(lambda elem: str(elem).lower().split(';')) + \
                          smellLike["характеристики"].map(lambda elem: str(elem).lower().split(';'))

itemAss = list(set(itertools.chain.from_iterable(smellLike["ассоциации"].values)))
itemAss.remove('nan')
itemAss.sort()

for item in itemAss:
    smellLike[item] = smellLike["ассоциации"].map(lambda elem: 1 if item in elem else 0)
del smellLike["ассоциации"]
del smellLike["характеристики"]
# ----------------------------------------------------------
sexDict = {"м": 0, "ж": 1}
df["пол"] = df["пол"].map(lambda elem: sexDict[elem])
# ----------------------------------------------------------
tailDict = {"крайне незаметный": 0, "незаметный": 0.25, "средний": 0.5, "заметный": 0.75, "очень заметный": 1}
df["шлейф"] = df["шлейф"].map(lambda elem: tailDict[elem])
# ----------------------------------------------------------
conDict = {"освежающая вода": 0, "одеколон": 0.2, "туалетная вода": 0.4, "парфюмерная вода": 0.6, "духи": 0.8,
           "масляные духи": 1}
df["концентрация"] = df["концентрация"].map(lambda elem: conDict[elem])
# ----------------------------------------------------------
countryDict = {"Франция": 0, "Италия": 1, "Испания":2, "США": 3, "Германия": 4}
# ----------------------------------------------------------
countryMatr = np.zeros((len(countryDict), len(countryDict)))
countryMatr[countryDict["Франция"]][countryDict["Италия"]] = countryMatr[countryDict["Италия"]][countryDict["Франция"]] = 0.5
countryMatr[countryDict["Франция"]][countryDict["США"]] = countryMatr[countryDict["США"]][countryDict["Франция"]] = 0.9
countryMatr[countryDict["Франция"]][countryDict["Испания"]] = countryMatr[countryDict["Испания"]][countryDict["Франция"]] = 0.8
countryMatr[countryDict["Франция"]][countryDict["Германия"]] = countryMatr[countryDict["Германия"]][countryDict["Франция"]] = 1

countryMatr[countryDict["Италия"]][countryDict["США"]] = countryMatr[countryDict["США"]][countryDict["Италия"]] = 0.5
countryMatr[countryDict["Италия"]][countryDict["Испания"]] = countryMatr[countryDict["Испания"]][countryDict["Италия"]] = 0.9
countryMatr[countryDict["Италия"]][countryDict["Германия"]] = countryMatr[countryDict["Германия"]][countryDict["Италия"]] = 1

countryMatr[countryDict["США"]][countryDict["Испания"]] = countryMatr[countryDict["Испания"]][countryDict["США"]] = 0.7
countryMatr[countryDict["США"]][countryDict["Германия"]] = countryMatr[countryDict["Германия"]][countryDict["США"]] = 1

countryMatr[countryDict["Испания"]][countryDict["Германия"]] = countryMatr[countryDict["Германия"]][countryDict["Испания"]] = 1
# ----------------------------------------------------------
df["верхние ноты"] = df["верхние ноты"].map(lambda elem: str(elem).lower().split(';'))
df["ноты сердца"] = df["ноты сердца"].map(lambda elem: str(elem).lower().split(';'))
df["базовые ноты"] = df["базовые ноты"].map(lambda elem: str(elem).lower().split(';'))
df["семейства"] = df["семейства"].map(lambda elem: str(elem).lower().split(';'))
# ----------------------------------------------------------
df["возраст (до 18)"] = df["возраст (до 18)"].map(lambda elem: 1 if elem == '+' else 0)
# ----------------------------------------------------------
df["стойкость минимум (ч)"] = df["стойкость минимум (ч)"].values / max(df["стойкость минимум (ч)"].values)
df["стойкость максимум (ч)"] = df["стойкость максимум (ч)"].values / max(df["стойкость максимум (ч)"].values)
# ----------------------------------------------------------
df["цена за 1 мл"] = df["цена"] / df["мл"]
df["цена за 1 мл"] = (df["цена за 1 мл"].values - min(df["цена за 1 мл"].values)) / (max(df["цена за 1 мл"].values) - min(df["цена за 1 мл"].values))
# ----------------------------------------------------------
itemSmells = list(set(itertools.chain.from_iterable(df["верхние ноты"].values)) |
             set(itertools.chain.from_iterable(df["ноты сердца"].values))  |
             set(itertools.chain.from_iterable(df["базовые ноты"].values)))
itemSmells.sort()

for item in itemSmells:
    df[item] = df["верхние ноты"].map(lambda elem: 1 if item in elem else 0) | \
               df["ноты сердца"].map(lambda elem: 1 if item in elem else 0) | \
               df["базовые ноты"].map(lambda elem: 1 if item in elem else 0) 
# ----------------------------------------------------------

itemFamily = list(set(itertools.chain.from_iterable(df["семейства"].values)))
for item in itemFamily:
    df[item + " семейства"] = df["семейства"].map(lambda elem: 1 if item in elem else 0)

for smell in smellLike.keys().drop('семейство'):
    df[smell] = df["семейства"].map(lambda elem:
        1 if sum(row[smell] for row in smellLike.iloc if row['семейство'] in elem) else 0)
# ----------------------------------------------------------

F_NAME = "название"
F_DIST = "расстояние"

nameArr = df["название"]

dfTree = pd.DataFrame(columns=["название", "семейства"], data=df[["название", "семейства"]].values)
# ----------------------------------------------------------

del df["верхние ноты"]
del df["ноты сердца"]
del df["базовые ноты"]
del df["семейства"]
del df["мл"]
del df["цена"]
del df["название"]
# ----------------------------------------------------------
layer1 = {"восточные": 0, "древесные": 1, "цветочные": 2, "фруктовые": 3}

treeLayer1 = np.zeros((len(layer1), len(layer1)))
treeLayer1[layer1["восточные"]][layer1["древесные"]] = treeLayer1[layer1["древесные"]][layer1["восточные"]] = 0.5
treeLayer1[layer1["восточные"]][layer1["цветочные"]] = treeLayer1[layer1["цветочные"]][layer1["восточные"]] = 0.7
treeLayer1[layer1["восточные"]][layer1["фруктовые"]] = treeLayer1[layer1["фруктовые"]][layer1["восточные"]] = 0.9
treeLayer1[layer1["древесные"]][layer1["цветочные"]] = treeLayer1[layer1["цветочные"]][layer1["древесные"]] = 0.7
treeLayer1[layer1["древесные"]][layer1["фруктовые"]] = treeLayer1[layer1["фруктовые"]][layer1["древесные"]] = 0.9
treeLayer1[layer1["цветочные"]][layer1["фруктовые"]] = treeLayer1[layer1["фруктовые"]][layer1["цветочные"]] = 0.7

layer2 = {"зеленые": 0, "цитрусовые": 1, "пряные": 2, "ванильные": 3, "фужерные": 4, "водные": 5, "мускусные": 6, "амбровые": 7, "сладкие": 8, "ароматические": 9, "-":10}

treeLayer2 = np.zeros((len(layer2), len(layer2)))
treeLayer2[layer2["зеленые"]][layer2["цитрусовые"]] = treeLayer2[layer2["цитрусовые"]][layer2["зеленые"]] = 0.5
treeLayer2[layer2["зеленые"]][layer2["пряные"]] = treeLayer2[layer2["пряные"]][layer2["зеленые"]] = 0.5
treeLayer2[layer2["зеленые"]][layer2["ванильные"]] = treeLayer2[layer2["ванильные"]][layer2["зеленые"]] = 0.3
treeLayer2[layer2["зеленые"]][layer2["фужерные"]] = treeLayer2[layer2["фужерные"]][layer2["зеленые"]] = 0.6
treeLayer2[layer2["зеленые"]][layer2["водные"]] = treeLayer2[layer2["водные"]][layer2["зеленые"]] = 0.5
treeLayer2[layer2["зеленые"]][layer2["мускусные"]] = treeLayer2[layer2["мускусные"]][layer2["зеленые"]] = 0.3
treeLayer2[layer2["зеленые"]][layer2["амбровые"]] = treeLayer2[layer2["амбровые"]][layer2["зеленые"]] = 0.3
treeLayer2[layer2["зеленые"]][layer2["сладкие"]] = treeLayer2[layer2["сладкие"]][layer2["зеленые"]] = 0.2
treeLayer2[layer2["зеленые"]][layer2["ароматические"]] = treeLayer2[layer2["ароматические"]][layer2["зеленые"]] = 0.3
treeLayer2[layer2["зеленые"]][layer2["-"]] = treeLayer2[layer2["-"]][layer2["зеленые"]] = 0.1

treeLayer2[layer2["цитрусовые"]][layer2["пряные"]] = treeLayer2[layer2["пряные"]][layer2["цитрусовые"]] = 0.4
treeLayer2[layer2["цитрусовые"]][layer2["ванильные"]] = treeLayer2[layer2["ванильные"]][layer2["цитрусовые"]] = 0.5
treeLayer2[layer2["цитрусовые"]][layer2["фужерные"]] = treeLayer2[layer2["фужерные"]][layer2["цитрусовые"]] = 0.3
treeLayer2[layer2["цитрусовые"]][layer2["водные"]] = treeLayer2[layer2["водные"]][layer2["цитрусовые"]] = 0.6
treeLayer2[layer2["цитрусовые"]][layer2["мускусные"]] = treeLayer2[layer2["мускусные"]][layer2["цитрусовые"]] = 0.5
treeLayer2[layer2["цитрусовые"]][layer2["амбровые"]] = treeLayer2[layer2["амбровые"]][layer2["цитрусовые"]] = 0.6
treeLayer2[layer2["цитрусовые"]][layer2["сладкие"]] = treeLayer2[layer2["сладкие"]][layer2["цитрусовые"]] = 0.4
treeLayer2[layer2["цитрусовые"]][layer2["ароматические"]] = treeLayer2[layer2["ароматические"]][layer2["цитрусовые"]] = 0.4
treeLayer2[layer2["цитрусовые"]][layer2["-"]] = treeLayer2[layer2["-"]][layer2["цитрусовые"]] = 0.1

treeLayer2[layer2["пряные"]][layer2["ванильные"]] = treeLayer2[layer2["ванильные"]][layer2["пряные"]] = 0.5
treeLayer2[layer2["пряные"]][layer2["фужерные"]] = treeLayer2[layer2["фужерные"]][layer2["пряные"]] = 0.3
treeLayer2[layer2["пряные"]][layer2["водные"]] = treeLayer2[layer2["водные"]][layer2["пряные"]] = 0.6
treeLayer2[layer2["пряные"]][layer2["мускусные"]] = treeLayer2[layer2["мускусные"]][layer2["пряные"]] = 0.6
treeLayer2[layer2["пряные"]][layer2["амбровые"]] = treeLayer2[layer2["амбровые"]][layer2["пряные"]] = 0.6
treeLayer2[layer2["пряные"]][layer2["сладкие"]] = treeLayer2[layer2["сладкие"]][layer2["пряные"]] = 0.3
treeLayer2[layer2["пряные"]][layer2["ароматические"]] = treeLayer2[layer2["ароматические"]][layer2["пряные"]] = 0.3
treeLayer2[layer2["пряные"]][layer2["-"]] = treeLayer2[layer2["-"]][layer2["пряные"]] = 0.1

treeLayer2[layer2["ванильные"]][layer2["фужерные"]] = treeLayer2[layer2["фужерные"]][layer2["ванильные"]] = 0.5
treeLayer2[layer2["ванильные"]][layer2["водные"]] = treeLayer2[layer2["водные"]][layer2["ванильные"]] = 0.7
treeLayer2[layer2["ванильные"]][layer2["мускусные"]] = treeLayer2[layer2["мускусные"]][layer2["ванильные"]] = 0.6
treeLayer2[layer2["ванильные"]][layer2["амбровые"]] = treeLayer2[layer2["амбровые"]][layer2["ванильные"]] = 0.4
treeLayer2[layer2["ванильные"]][layer2["сладкие"]] = treeLayer2[layer2["сладкие"]][layer2["ванильные"]] = 0.3
treeLayer2[layer2["ванильные"]][layer2["ароматические"]] = treeLayer2[layer2["ароматические"]][layer2["ванильные"]] = 0.5
treeLayer2[layer2["ванильные"]][layer2["-"]] = treeLayer2[layer2["-"]][layer2["ванильные"]] = 0.1

treeLayer2[layer2["фужерные"]][layer2["водные"]] = treeLayer2[layer2["водные"]][layer2["фужерные"]] = 0.7
treeLayer2[layer2["фужерные"]][layer2["мускусные"]] = treeLayer2[layer2["мускусные"]][layer2["фужерные"]] = 0.7
treeLayer2[layer2["фужерные"]][layer2["амбровые"]] = treeLayer2[layer2["амбровые"]][layer2["фужерные"]] = 0.7
treeLayer2[layer2["фужерные"]][layer2["сладкие"]] = treeLayer2[layer2["сладкие"]][layer2["фужерные"]] = 0.5
treeLayer2[layer2["фужерные"]][layer2["ароматические"]] = treeLayer2[layer2["ароматические"]][layer2["фужерные"]] = 0.5
treeLayer2[layer2["фужерные"]][layer2["-"]] = treeLayer2[layer2["-"]][layer2["фужерные"]] = 0.1

treeLayer2[layer2["водные"]][layer2["мускусные"]] = treeLayer2[layer2["мускусные"]][layer2["водные"]] = 0.3
treeLayer2[layer2["водные"]][layer2["амбровые"]] = treeLayer2[layer2["амбровые"]][layer2["водные"]] = 0.7
treeLayer2[layer2["водные"]][layer2["сладкие"]] = treeLayer2[layer2["сладкие"]][layer2["водные"]] = 0.6
treeLayer2[layer2["водные"]][layer2["ароматические"]] = treeLayer2[layer2["ароматические"]][layer2["водные"]] = 0.6
treeLayer2[layer2["водные"]][layer2["-"]] = treeLayer2[layer2["-"]][layer2["водные"]] = 0.1

treeLayer2[layer2["мускусные"]][layer2["амбровые"]] = treeLayer2[layer2["амбровые"]][layer2["мускусные"]] = 0.5
treeLayer2[layer2["мускусные"]][layer2["сладкие"]] = treeLayer2[layer2["сладкие"]][layer2["мускусные"]] = 0.6
treeLayer2[layer2["мускусные"]][layer2["ароматические"]] = treeLayer2[layer2["ароматические"]][layer2["мускусные"]] = 0.3
treeLayer2[layer2["мускусные"]][layer2["-"]] = treeLayer2[layer2["-"]][layer2["мускусные"]] = 0.1

treeLayer2[layer2["амбровые"]][layer2["сладкие"]] = treeLayer2[layer2["сладкие"]][layer2["амбровые"]] = 0.3
treeLayer2[layer2["амбровые"]][layer2["ароматические"]] = treeLayer2[layer2["ароматические"]][layer2["амбровые"]] = 0.3
treeLayer2[layer2["амбровые"]][layer2["-"]] = treeLayer2[layer2["-"]][layer2["амбровые"]] = 0.1

treeLayer2[layer2["сладкие"]][layer2["ароматические"]] = treeLayer2[layer2["ароматические"]][layer2["сладкие"]] = 0.6
treeLayer2[layer2["сладкие"]][layer2["-"]] = treeLayer2[layer2["-"]][layer2["сладкие"]] = 0.1

treeLayer2[layer2["-"]][layer2["ароматические"]] = treeLayer2[layer2["-"]][layer2["ароматические"]] = 0.1

layer3 = {"свежие": 0, "мускусные": 1, "шипровые": 2, "пряные": 3, "-": 4}

treeLayer3 = np.zeros((len(layer3), len(layer3)))
treeLayer3[layer3["свежие"]][layer3["мускусные"]] = treeLayer3[layer3["мускусные"]][layer3["свежие"]] = 0.7
treeLayer3[layer3["свежие"]][layer3["шипровые"]] = treeLayer3[layer3["шипровые"]][layer3["свежие"]] = 0.7
treeLayer3[layer3["свежие"]][layer3["пряные"]] = treeLayer3[layer3["пряные"]][layer3["свежие"]] = 0.7
treeLayer3[layer3["свежие"]][layer3["-"]] = treeLayer3[layer3["-"]][layer3["свежие"]] = 1

treeLayer3[layer3["мускусные"]][layer3["шипровые"]] = treeLayer3[layer3["шипровые"]][layer3["мускусные"]] = 0.2
treeLayer3[layer3["мускусные"]][layer3["пряные"]] = treeLayer3[layer3["пряные"]][layer3["мускусные"]] = 0.6
treeLayer3[layer3["мускусные"]][layer3["-"]] = treeLayer3[layer3["-"]][layer3["мускусные"]] = 1

treeLayer3[layer3["шипровые"]][layer3["пряные"]] = treeLayer3[layer3["пряные"]][layer3["шипровые"]] = 0.6
treeLayer3[layer3["шипровые"]][layer3["-"]] = treeLayer3[layer3["-"]][layer3["шипровые"]] = 1

treeLayer3[layer3["пряные"]][layer3["-"]] = treeLayer3[layer3["-"]][layer3["пряные"]] = 1

layer = [layer1, layer2, layer3]
tree = [treeLayer1, treeLayer2, treeLayer3]
# ----------------------------------------------------------

excludeFields = ["стойкость минимум (ч)", "стойкость максимум (ч)", "возраст (до 18)", 
                 "цена за 1 мл", "пол", "бренд",
                 "страна", "концентрация"]

def getDataFrameAroma(df):
    dfNew = df.copy()
    for elem in excludeFields:
        del dfNew[elem]
    return dfNew

def getDataFrameStat(df):
    dfStatParams = pd.DataFrame(columns=excludeFields, data=df[excludeFields].values)
    del dfStatParams["бренд"]
    del dfStatParams["страна"]
    return dfStatParams
# ----------------------------------------------------------
# Расстояния

def _complete(v1, v2):
    for i in range(len(v1) - len(v2)):
        v2.append("-")
    return v2

def complete(v1, v2):
    n1, n2 = len(v1), len(v2)
    if n1 > n2:
        v2 = _complete(v1, v2)
    elif n1 < n2:
        v1 = _complete(v2, v1)
    return v1, v2

# Расстояния
def getDistance(v1, v2, nPow):
    res = 0
    for i in range(len(v1)):
        if isnan(v1[i]) or isnan(v2[i]):
            continue
        res += pow(abs(v1[i] - v2[i]), nPow)
    return pow(res, 1 / nPow)

# Манхэттенское расстояние
def getManhattanDistance(v1, v2):
    return getDistance(v1, v2, 1)

# Евклидово расстояние
def getEuclideanDistance(v1, v2):
    return getDistance(v1, v2, 2)

# Косинусное
def getCos(v1, v2):
    v1T, v2T = v1.copy(), v2.copy()
    n = len(v1)
    indArr = [i for i, (elem1, elem2) in enumerate(zip(v1T, v2T)) if isnan(elem1) or isnan(elem2)]
    v1T[:] = [elem for i, elem in enumerate(v1T) if i not in indArr]
    v2T[:] = [elem for i, elem in enumerate(v2T) if i not in indArr]
    return 1 - dot(v1T, v2T) / (norm(v1T) * norm(v2T))

# Расстояние по дереву
def getTreeDistance(v1, v2):
    res = 0
    resArr = []
    v1T, v2T = v1, v2
    if len(v1) != len(v2):
        v1T, v2T = complete(v1, v2)
    for i in range(len(v1T)):
        res += tree[i][layer[i][v1T[i]]][layer[i][v2T[i]]]
    return res / len(tree)

# Сравнение брендов
def getBrandDistance(v1, v2):
    return 0 if v1[0] == v2[0] else 1

# Сравнение стран
def getCountryDistance(v1, v2):
    return countryMatr[countryDict[v1]][countryDict[v2]]

# Найти все похожие
def getSimilarity(id, matr, nameArr):
    data = matr[id]
    res = pd.DataFrame(zip(data, nameArr), index=np.arange(len(matr)), columns=["расстояние", "название"])
    return res.sort_values("расстояние")
# ----------------------------------------------------------
# Меры
# Мера Жаккара
def _getJacquard(v1, v2):
    a = v1.count(1)
    b = v2.count(1)
    c = 0
    for i in range(len(v1)):
        if v1[i] and v2[i]:
            c += 1
    return 1 - c / (a + b - c)

def getJacquard(df, nameArr):
    matrData = df.values.tolist()
    n = len(matrData)
    matrRes = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            matrRes[i][j] = matrRes[j][i] = _getJacquard(matrData[i], matrData[j])
    return matrRes
# ----------------------------------------------------------
# Подсчёт расстояний
def calcDistance(f, df):
    matrData = df.values.tolist()
    n = len(matrData)
    matrRes = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            matrRes[i][j] = matrRes[j][i] = f(matrData[i], matrData[j])
    return matrRes / matrRes.max()

def calcDistanceCompined(df, dfTree):
    dfTree = dfTree["семейства"]
    dfMan = getDataFrameAroma(df)
    dfJac = dfMan.copy()
    del dfJac["шлейф"]

    dfStatParams = getDataFrameStat(df)

    matrTree = calcDistance(getTreeDistance, dfTree)
    matrEucl = calcDistance(getEuclideanDistance, dfStatParams)
    matrBrand = calcDistance(getBrandDistance, df["бренд"])
    matrCountry = calcDistance(getCountryDistance, df["страна"])
    matrJac = getJacquard(dfJac, nameArr)

    xTree = matrTree.max()
    xEuci = matrEucl.max()
    xJac = matrJac.max()
    xBrand = matrBrand.max()
    xCountry = matrCountry.max()

    kJac, kTree, kEuci, kBrand, kCountry = 2, 0.5, 10, 2, 2

    return (kJac * matrJac + kTree * matrTree + matrEucl + kBrand * matrBrand + kCountry * matrCountry) / (
                kJac * xJac + kTree * xTree + xEuci + kBrand * xBrand + kCountry * xCountry)
# ----------------------------------------------------------
matrSimilarity = calcDistanceCompined(df, dfTree)
# ----------------------------------------------------------
# Найти похожий на другой парфюм
def _findSimilar(name):
    ind = df0[F_NAME].tolist().index(name)
    listSimilarity = getSimilarity(ind, matrSimilarity, nameArr)
    return listSimilarity

def findSimilar(name):
    listSimilarity = _findSimilar(name)
    return listSimilarity[listSimilarity[F_NAME] != name]
# ----------------------------------------------------------
# Найти похожий на другие парфюмы (вход - несколько ароматов)
def _findSimilarMany(nameArr):
    recList = []
    for name in nameArr:
        rec = _findSimilar(name)
        recList.append(rec.loc[rec[F_NAME].isin(nameArr) == False])
    dfRes = defaultdict(lambda: 1e2)
    for rec in recList:
        for i, row in rec.iterrows():
            curName = row[F_NAME]
            curDist = row[F_DIST]
            dfRes[curName] = min(dfRes[curName], curDist)
    return dfRes

def findSimilarMany(nameArr):
    resDict = _findSimilarMany(nameArr)
    return sorted([{key: elem} for key, elem in resDict.items()], key=lambda elem: list(elem.values())[0])
# ----------------------------------------------------------
# Массив лайков и дизлайков
def delOpposite(dict, nameArr):
    for name in nameArr:
        if name in dict.keys():
            del dict[name]
    return dict

def findSimilar(likesArr, dislikesArr):
    likesRec = delOpposite(_findSimilarMany(likesArr), dislikesArr)
    dislikesRec = delOpposite(_findSimilarMany(dislikesArr), likesArr)
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
# ----------------------------------------------------------
def sortDict(resDict):
    sorted_tuples = sorted(resDict.items(), key=lambda item: item[1], reverse=True)
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict

def getArrFromSeries(data):
    arr = []
    for elem in data:
        arr.append(elem)
    return arr

def _fromArrDictToDict(arrDict):
    resDict = {}
    for elem in arrDict:
        resDict.update(elem)
    return resDict

def _compareLikesParams(likesDict, paramsDict):
    resDict = {}
    for key, value in likesDict.items():
        if key in paramsDict.keys():
            resDict[key] = (value + paramsDict[key]) * 0.5
            del paramsDict[key]
        else:
            resDict[key] = value * 0.5
    if len(paramsDict.keys()):
        for key, value in paramsDict.items():
            resDict[key] = 0.5 * value
    return resDict
namesUI = getArrFromSeries(nameArr)
# ----------------------------------------------------------
def _getDefaultResultParams(nameArr):
    resArr = {}
    for name in nameArr:
        resArr[name] = 0
    return resArr

def _getRecommendationParams(sexSelected, countrySelected, brandSelected,
                            conSelected, familySelected, smellSelected,
                             durabilitySelected, df):
    dfColumnsArr = df.columns.values.tolist()
    indexDict = {}
    indexDict[dfColumnsArr.index('пол')] = sexSelected
    indexDict[dfColumnsArr.index('страна')] = countrySelected
    indexDict[dfColumnsArr.index('бренд')] = brandSelected
    indexDict[dfColumnsArr.index('концентрация')] = conSelected
    indexDict[dfColumnsArr.index('стойкость минимум (ч)')] = durabilitySelected
    for family in familySelected:
        indexDict[dfColumnsArr.index(family)] = [1]
    for smell in smellSelected:
        indexDict[dfColumnsArr.index(smell)] = [1]
    matrData = df.values.tolist()
    sDict = {}
    for i in range(len(matrData)):
        s = 0
        for ind in indexDict.keys():
            if matrData[i][ind] in indexDict[ind]:
                s += 1
        sDict[i] = s
    return sDict

def _updateResult(dataDict, nameArr, n):
    resDict = {}
    for key, value in dataDict.items():
        if value == 0:
            continue
        resDict[nameArr[key]] = value / n
    return sortDict(resDict)

def getRecommendationParams(sexSelected, countrySelected, brandSelected,
                            conSelected, familySelected, smellSelected,
                            durabilitySelected, df):
    nAll = 0
    if len(sexSelected):
        nAll += 1
    if len(countrySelected):
        nAll += 1
    if len(brandSelected):
        nAll += 1
    if len(conSelected):
        nAll += 1
    if len(durabilitySelected):
        nAll += 1
    nAll += len(familySelected) + len(smellSelected)
    if nAll == 0:
        recDict = _getDefaultResultParams(namesUI)
    else:
        recDict = _getRecommendationParams(sexSelected, countrySelected, brandSelected, conSelected, familySelected,
                                           smellSelected, durabilitySelected, df)
        recDict = _updateResult(recDict, nameArr, nAll)
    return recDict
def _getDefaultResult(nameArr):
    resArr = []
    for name in nameArr:
        resArr.append({name: 1})
    return resArr
def _getRecommendationArr(likesArr, dislikesArr):
    recArr = None

    if len(likesArr) and len(dislikesArr):
        recArr = findSimilar(likesArr, dislikesArr)
    elif len(likesArr) and len(dislikesArr) == 0:
        recArr = findSimilarMany(likesArr)
    elif len(likesArr) == 0 and len(dislikesArr):
        recArr = findSimilar(likesArr, dislikesArr)
    else:
        recArr = _getDefaultResult(namesUI)
    return recArr

def _splitMustMaybeDictArr(recDict):
    recMust, recMaybe = [], []
    for name, value in recDict.items():
        if value >= 0.5:
            recMust.append(name)
        else:
            recMaybe.append(name)
    return recMust, recMaybe

def giveRecommendationFull(sexSelected, countrySelected, brandSelected,
                            conSelected, familySelected, smellSelected,
                           likesSelected, dislikesSelected, durabilitySelected,df):
    recDict = getRecommendationParams(sexSelected, countrySelected, brandSelected, conSelected, familySelected, smellSelected, durabilitySelected, df)
    if len(likesSelected) or len(dislikesSelected):
        recLikesArr = _getRecommendationArr(likesSelected, dislikesSelected)
        recLikesDict = _fromArrDictToDict(recLikesArr)
        recDict = _compareLikesParams(recLikesDict, recDict)
    return _splitMustMaybeDictArr(sortDict(recDict))
