from cmath import isnan, nan
from numpy import dot
from numpy.linalg import norm
import pandas as pd
import numpy as np
import plotly.express as px
from preprocessing import *

excludeFields = ["Стойкость минимум (ч)", "Стойкость максимум (ч)", "Возраст (до 18)", "цена за 1 мл", "Пол", "Бренд", 
                 "Страна", "Концентрация"]

def getDataFrameAroma(df):
    dfNew = df.copy()
    for elem in excludeFields:
        del dfNew[elem]
    return dfNew

def getDataFrameStat(df):
    dfStatParams = pd.DataFrame(columns=excludeFields, data=df[excludeFields].values)
    del dfStatParams["Бренд"]
    del dfStatParams["Страна"]

    return dfStatParams

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
    layer, tree = make_tree_and_layer()
    res = 0
    # resArr = []
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
    countryMatr, countryDict = make_countryMatr_and_countryDict()
    return countryMatr[countryDict[v1]][countryDict[v2]]

# Найти все похожие
def getSimilarity(id, matr, nameArr):
    data = matr[id]
    res = pd.DataFrame(zip(data, nameArr), index=np.arange(len(matr)), columns=["расстояние", "Название"])
    return res.sort_values("расстояние")

def _getJacquard(v1, v2):
    a = v1.count(1)
    b = v2.count(1)
    c = 0
    for i in range(len(v1)):
        if v1[i] and v2[i]:
            c += 1
    return 1 - c / (a + b - c)

# Мера Жаккара
def getJacquard(df):
    matrData = df.values.tolist()
    n = len(matrData)
    matrRes = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            matrRes[i][j] = matrRes[j][i] = _getJacquard(matrData[i], matrData[j])
    return matrRes

def calcDistance(f, df):
    matrData = df.values.tolist()
    n = len(matrData)
    matrRes = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            matrRes[i][j] = matrRes[j][i] = f(matrData[i], matrData[j])
    return matrRes / matrRes.max()   


def calcDistanceCompined(df, dfTree, nameArr):
    dfTree = dfTree["Семейства"]
    dfMan = getDataFrameAroma(df)
    dfJac = dfMan.copy()
    del dfJac["Шлейф"]

    dfStatParams = getDataFrameStat(df)
    
    matrTree = calcDistance(getTreeDistance, dfTree)
    # matrCos = calcDistance(getCos, dfMan)
    matrEucl = calcDistance(getEuclideanDistance, dfStatParams)
    # matrMan = calcDistance(getManhattanDistance, dfMan)
    matrBrand = calcDistance(getBrandDistance, df["Бренд"])
    matrCountry = calcDistance(getCountryDistance, df["Страна"])
    matrJac = getJacquard(dfJac)

    xTree = matrTree.max()
    # xCos = matrCos.max()
    xEuci = matrEucl.max()
    # xMan = matrMan.max()
    xJac = matrJac.max()
    xBrand = matrBrand.max()
    xCountry = matrCountry.max()


    kJac, kTree, kEuci, kBrand, kCountry = 2, 0.5, 10, 2, 2

    return (kJac * matrJac + kTree * matrTree + matrEucl + kBrand * matrBrand + kCountry * matrCountry) / (kJac * xJac + kTree * xTree + xEuci + kBrand * xBrand + kCountry * xCountry)

def draw(matrRes, nameArr, title, color='Inferno'):
    fig = px.imshow(matrRes, x=nameArr, y=nameArr, color_continuous_scale=color, title=title)
    fig.update_layout(width=1000, height=1200)
    fig.update_traces(text=nameArr)
    fig.update_xaxes(side="top")
    fig.show()