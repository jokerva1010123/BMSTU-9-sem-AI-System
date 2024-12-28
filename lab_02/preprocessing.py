import pandas as pd
import numpy as np
import itertools
import math
from IPython.display import display

from turtle import color
from unicodedata import name
import plotly.figure_factory as ff
import matplotlib.pyplot as plt

def preprocessing():

    pd.set_option('display.max_columns', None)
    df0 = pd.read_csv('dataset.csv', delimiter=',', encoding="utf8")
    df = df0.copy(deep=True)

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

    # print(smellLike)

    sexDict = { "м": 0, "ж": 1 }
    df["Пол"] = df["Пол"].map(lambda elem: sexDict[elem])
    tailDict = { "крайне незаметный": 0, "незаметный": 0.25, "средний": 0.5, "заметный": 0.75, "очень заметный": 1}
    df["Шлейф"] = df["Шлейф"].map(lambda elem: tailDict[elem])
    conDict = {"освежающая вода": 0, "одеколон": 0.2, "туалетная вода": 0.4, "парфюмерная вода": 0.6, "духи": 0.8, "масляные духи": 1}
    df["Концентрация"] = df["Концентрация"].map(lambda elem: conDict[elem])

    df["верхние ноты"] = df["верхние ноты"].map(lambda elem: str(elem).lower().split(';'))
    df["ноты сердца"] = df["ноты сердца"].map(lambda elem: str(elem).lower().split(';'))
    df["базовые ноты"] = df["базовые ноты"].map(lambda elem: str(elem).lower().split(';'))
    df["Семейства"] = df["Семейства"].map(lambda elem: str(elem).lower().split(';'))
    # df["характеристики аромата"] = df["характеристики аромата"].map(lambda elem: str(elem).lower().split(';'))

    df["Возраст (до 18)"] = df["Возраст (до 18)"].map(lambda elem: 1 if elem == '+' else 0)

    df["Стойкость минимум (ч)"] = df["Стойкость минимум (ч)"].values / max(df["Стойкость минимум (ч)"].values)
    df["Стойкость максимум (ч)"] = df["Стойкость максимум (ч)"].values / max(df["Стойкость максимум (ч)"].values)

    df["цена за 1 мл"] = df["Цена"] / df["мл"]
    df["цена за 1 мл"] = (df["цена за 1 мл"].values - min(df["цена за 1 мл"].values)) / (max(df["цена за 1 мл"].values) - min(df["цена за 1 мл"].values))

    itemSmells = list(set(itertools.chain.from_iterable(df["верхние ноты"].values)) | 
                set(itertools.chain.from_iterable(df["ноты сердца"].values))  |
                set(itertools.chain.from_iterable(df["базовые ноты"].values)))
    itemSmells.sort()
    # itemSmells.remove('nan')
    for item in itemSmells:
        df[item] = df["верхние ноты"].map(lambda elem: 1 if item in elem else 0) | \
                df["ноты сердца"].map(lambda elem: 1 if item in elem else 0) | \
                df["базовые ноты"].map(lambda elem: 1 if item in elem else 0) 

    itemFamily = list(set(itertools.chain.from_iterable(df["Семейства"].values)))
    for item in itemFamily:
        df[item + " Семейства"] = df["Семейства"].map(lambda elem: 1 if item in elem else 0)
    # print(itemFamily)
    for smell in smellLike.keys().drop('семейство'):
        df[smell] = df["Семейства"].map(lambda elem:
            1 if sum(row[smell] for row in smellLike.iloc if row['семейство'] in elem) else 0)
        
    F_NAME = "название"
    F_DIST = "расстояние"

    nameArr = df["Название"]

    dfTree = pd.DataFrame(columns=["Название", "Семейства"], data=df[["Название", "Семейства"]].values)

    del df["верхние ноты"]
    del df["ноты сердца"]
    del df["базовые ноты"]
    # del df["запахи"]
    del df["Семейства"]
    # del df["время года"]
    # del df["характеристики аромата"]
    del df["мл"]
    del df["Цена"]
    del df["Название"]
    # display(df)
    # display(df)
    return df, dfTree, nameArr

def make_countryMatr_and_countryDict():
    countryDict = {"Франция": 0, "Италия": 1, "Испания":2, "США": 3, "Германия": 4}

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
    return countryMatr, countryDict

def make_tree_and_layer():
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
    return layer, tree