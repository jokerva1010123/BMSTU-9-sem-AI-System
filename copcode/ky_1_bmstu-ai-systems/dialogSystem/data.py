import pandas as pd
import numpy as np
import itertools
from cmath import isnan
from numpy import dot
from numpy.linalg import norm
from collections import defaultdict
import plotly.express as px

from color import *


pd.set_option('display.max_columns', None)
df0 = pd.read_csv('../docs/data2.csv', delimiter=';', encoding="utf8")
df = df0.copy(deep=True)

genderDict = { "м": 0, "ж": 1 }
sizeDict = { "S": 42, "M": 44, "L": 46, "XL": 48, "XXL": 50 }
df["Пол"] = df["Пол"].map(lambda elem: genderDict[elem])
df["Размер"] = df["Размер"].map(lambda elem: sizeDict[elem])
df["Иерархия"] = df["Иерархия"].map(lambda elem: elem.split(","))

hierarchyList = list(set(itertools.chain.from_iterable(df["Иерархия"].values)))
for item in hierarchyList:
    df[item] = df["Иерархия"].map(lambda elem: 1 if item in elem else 0)

df["Очень низкая стоимость"] = df["Цена"].map(lambda elem: 1 if elem <= 1800 else 0)
df["Низкая стоимость"] = df["Цена"].map(lambda elem: 1 if 1800 < elem <= 2900 else 0)
df["Средняя стоимость"] = df["Цена"].map(lambda elem: 1 if 2900 < elem <= 5200 else 0)
df["Высокая стоимость"] = df["Цена"].map(lambda elem: 1 if 5200 < elem <= 6900 else 0)
df["Очень высокая стоимость"] = df["Цена"].map(lambda elem: 1 if 6900 < elem else 0)


F_NAME = "Название"
F_DIST = "Расстояние"

nameArr = df["Название"]

dfTree = pd.DataFrame(
    columns=["Название", "Иерархия"], 
    data=df[["Название", "Иерархия"]].values
)

del df["Название"]
del df["Иерархия"]

businessBrands = {
    "Briony": 0,
    "Corneliani": 1,
    "Hugo Boss": 2,
    "Canali": 3,
}
everydayBrands = {
    "H&M": 4,
    "Zara": 5,
    "Levi's": 6,
    "Lacoste": 7,
}
sportsBrands = {
    "Nike": 8,
    "Adidas": 9,
    "Puma": 10,
    "Reebok": 11,
}
brands = {
    **businessBrands,
    **everydayBrands,
    **sportsBrands,
}

countBrands = len(businessBrands) + len(everydayBrands) + len(sportsBrands)
brandsMatr = np.zeros((countBrands, countBrands))

for businessBrandKey in businessBrands.keys():
    for _businessBrandKey in businessBrands.keys():
        if _businessBrandKey != businessBrandKey:
            brandsMatr[businessBrands[businessBrandKey], businessBrands[_businessBrandKey]] = \
            brandsMatr[businessBrands[_businessBrandKey], businessBrands[businessBrandKey]] = 0.1

    for everydayBrandKey in everydayBrands.keys():
        brandsMatr[businessBrands[businessBrandKey], everydayBrands[everydayBrandKey]] = \
        brandsMatr[everydayBrands[everydayBrandKey], businessBrands[businessBrandKey]] = 0.6

    for sportsBrandKey in sportsBrands.keys():
        brandsMatr[businessBrands[businessBrandKey], sportsBrands[sportsBrandKey]] = \
        brandsMatr[sportsBrands[sportsBrandKey], businessBrands[businessBrandKey]] = 1

for everydayBrandKey in everydayBrands.keys():
    for _everydayBrandKey in everydayBrands.keys():
        if _everydayBrandKey != everydayBrandKey:
            brandsMatr[everydayBrands[everydayBrandKey], everydayBrands[_everydayBrandKey]] = \
            brandsMatr[everydayBrands[_everydayBrandKey], everydayBrands[everydayBrandKey]] = 0.1
            
    for sportsBrandKey in sportsBrands.keys():
        brandsMatr[everydayBrands[everydayBrandKey], sportsBrands[sportsBrandKey]] = \
        brandsMatr[sportsBrands[sportsBrandKey], everydayBrands[everydayBrandKey]] = 0.4

for sportsBrandKey in sportsBrands.keys():
    for _sportsBrandKey in sportsBrands.keys():
        if _sportsBrandKey != sportsBrandKey:
            brandsMatr[sportsBrands[sportsBrandKey], sportsBrands[_sportsBrandKey]] = \
            brandsMatr[sportsBrands[_sportsBrandKey], sportsBrands[sportsBrandKey]] = 0.1

colors = {
    "Белый": 0,
    "Черный": 1,
    "Серый": 2,
    "Синий": 3,
    "Голубой": 4,
    "Красный": 5,
    "Розовый": 6
}

colorsMatr = np.zeros((len(colors), len(colors)))

colorsMatr[colors["Белый"], colors["Черный"]] = colorsMatr[colors["Черный"], colors["Белый"]] = 1
colorsMatr[colors["Белый"], colors["Серый"]] = colorsMatr[colors["Серый"], colors["Белый"]] = 0.5
colorsMatr[colors["Белый"], colors["Синий"]] = colorsMatr[colors["Синий"], colors["Белый"]] = 0.7
colorsMatr[colors["Белый"], colors["Голубой"]] = colorsMatr[colors["Голубой"], colors["Белый"]] = 0.4
colorsMatr[colors["Белый"], colors["Красный"]] = colorsMatr[colors["Красный"], colors["Белый"]] = 0.7
colorsMatr[colors["Белый"], colors["Розовый"]] = colorsMatr[colors["Розовый"], colors["Белый"]] = 0.4

colorsMatr[colors["Черный"], colors["Серый"]] = colorsMatr[colors["Серый"], colors["Черный"]] = 0.3
colorsMatr[colors["Черный"], colors["Синий"]] = colorsMatr[colors["Синий"], colors["Черный"]] = 0.6
colorsMatr[colors["Черный"], colors["Голубой"]] = colorsMatr[colors["Голубой"], colors["Черный"]] = 1
colorsMatr[colors["Черный"], colors["Красный"]] = colorsMatr[colors["Красный"], colors["Черный"]] = 0.6
colorsMatr[colors["Черный"], colors["Розовый"]] = colorsMatr[colors["Розовый"], colors["Черный"]] = 1

colorsMatr[colors["Серый"], colors["Синий"]] = colorsMatr[colors["Синий"], colors["Серый"]] = 0.8
colorsMatr[colors["Серый"], colors["Голубой"]] = colorsMatr[colors["Голубой"], colors["Серый"]] = 1
colorsMatr[colors["Серый"], colors["Красный"]] = colorsMatr[colors["Красный"], colors["Серый"]] = 0.8
colorsMatr[colors["Серый"], colors["Розовый"]] = colorsMatr[colors["Розовый"], colors["Серый"]] = 1

colorsMatr[colors["Синий"], colors["Голубой"]] = colorsMatr[colors["Голубой"], colors["Синий"]] = 0.3
colorsMatr[colors["Синий"], colors["Красный"]] = colorsMatr[colors["Красный"], colors["Синий"]] = 0.7
colorsMatr[colors["Синий"], colors["Розовый"]] = colorsMatr[colors["Розовый"], colors["Синий"]] = 1

colorsMatr[colors["Голубой"], colors["Красный"]] = colorsMatr[colors["Красный"], colors["Голубой"]] = 1
colorsMatr[colors["Голубой"], colors["Розовый"]] = colorsMatr[colors["Розовый"], colors["Голубой"]] = 0.7

colorsMatr[colors["Красный"], colors["Розовый"]] = colorsMatr[colors["Розовый"], colors["Красный"]] = 0.3

layer1 = {
    "Деловая одежда": 0,
    "Спортивная одежда": 1,
    "Повседневная одежда": 2,
}

treeLayer1 = np.zeros((len(layer1), len(layer1)))

treeLayer1[layer1["Деловая одежда"], layer1["Спортивная одежда"]] = treeLayer1[layer1["Спортивная одежда"], layer1["Деловая одежда"]] = 1
treeLayer1[layer1["Деловая одежда"], layer1["Повседневная одежда"]] = treeLayer1[layer1["Повседневная одежда"], layer1["Деловая одежда"]] = 0.6

treeLayer1[layer1["Спортивная одежда"], layer1["Повседневная одежда"]] = treeLayer1[layer1["Повседневная одежда"], layer1["Спортивная одежда"]] = 0.4

layer2 = {
    "Пиджаки": 0,
    "Брюки": 1,
    "Рубашки": 2,
    "Спортивные футболки": 3,
    "Спортивные шорты": 4,
    "Спортивные брюки": 5,
    "Спортивные толстовки": 6,
    "Свитеры и кофты": 7,
    "Футболки": 8,
    "Лонгсливы": 9,
    "Джинсы": 10,
    "Шорты": 11,
}

treeLayer2 = np.zeros((len(layer2), len(layer2)))


treeLayer2[layer2["Пиджаки"], layer2["Брюки"]] = treeLayer2[layer2["Брюки"], layer2["Пиджаки"]] = 0.3
treeLayer2[layer2["Пиджаки"], layer2["Рубашки"]] = treeLayer2[layer2["Рубашки"], layer2["Пиджаки"]] = 0.2
treeLayer2[layer2["Пиджаки"], layer2["Спортивные футболки"]] = treeLayer2[layer2["Спортивные футболки"], layer2["Пиджаки"]] = 1
treeLayer2[layer2["Пиджаки"], layer2["Спортивные шорты"]] = treeLayer2[layer2["Спортивные шорты"], layer2["Пиджаки"]] = 1
treeLayer2[layer2["Пиджаки"], layer2["Спортивные брюки"]] = treeLayer2[layer2["Спортивные брюки"], layer2["Пиджаки"]] = 1
treeLayer2[layer2["Пиджаки"], layer2["Спортивные толстовки"]] = treeLayer2[layer2["Спортивные толстовки"], layer2["Пиджаки"]] = 1
treeLayer2[layer2["Пиджаки"], layer2["Свитеры и кофты"]] = treeLayer2[layer2["Свитеры и кофты"], layer2["Пиджаки"]] = 0.7
treeLayer2[layer2["Пиджаки"], layer2["Футболки"]] = treeLayer2[layer2["Футболки"], layer2["Пиджаки"]] = 0.6
treeLayer2[layer2["Пиджаки"], layer2["Лонгсливы"]] = treeLayer2[layer2["Лонгсливы"], layer2["Пиджаки"]] = 0.6
treeLayer2[layer2["Пиджаки"], layer2["Джинсы"]] = treeLayer2[layer2["Джинсы"], layer2["Пиджаки"]] = 0.5
treeLayer2[layer2["Пиджаки"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Пиджаки"]] = 1

treeLayer2[layer2["Брюки"], layer2["Рубашки"]] = treeLayer2[layer2["Рубашки"], layer2["Брюки"]] = 0.3
treeLayer2[layer2["Брюки"], layer2["Спортивные футболки"]] = treeLayer2[layer2["Спортивные футболки"], layer2["Брюки"]] = 0.9
treeLayer2[layer2["Брюки"], layer2["Спортивные шорты"]] = treeLayer2[layer2["Спортивные шорты"], layer2["Брюки"]] = 1
treeLayer2[layer2["Брюки"], layer2["Спортивные брюки"]] = treeLayer2[layer2["Спортивные брюки"], layer2["Брюки"]] = 1
treeLayer2[layer2["Брюки"], layer2["Спортивные толстовки"]] = treeLayer2[layer2["Спортивные толстовки"], layer2["Брюки"]] = 0.8
treeLayer2[layer2["Брюки"], layer2["Свитеры и кофты"]] = treeLayer2[layer2["Свитеры и кофты"], layer2["Брюки"]] = 0.9
treeLayer2[layer2["Брюки"], layer2["Футболки"]] = treeLayer2[layer2["Футболки"], layer2["Брюки"]] = 0.7
treeLayer2[layer2["Брюки"], layer2["Лонгсливы"]] = treeLayer2[layer2["Лонгсливы"], layer2["Брюки"]] = 0.7
treeLayer2[layer2["Брюки"], layer2["Джинсы"]] = treeLayer2[layer2["Джинсы"], layer2["Брюки"]] = 0.6
treeLayer2[layer2["Брюки"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Брюки"]] = 1

treeLayer2[layer2["Рубашки"], layer2["Спортивные футболки"]] = treeLayer2[layer2["Спортивные футболки"], layer2["Рубашки"]] = 1
treeLayer2[layer2["Рубашки"], layer2["Спортивные шорты"]] = treeLayer2[layer2["Спортивные шорты"], layer2["Рубашки"]] = 1
treeLayer2[layer2["Рубашки"], layer2["Спортивные брюки"]] = treeLayer2[layer2["Спортивные брюки"], layer2["Рубашки"]] = 1
treeLayer2[layer2["Рубашки"], layer2["Спортивные толстовки"]] = treeLayer2[layer2["Спортивные толстовки"], layer2["Рубашки"]] = 1
treeLayer2[layer2["Рубашки"], layer2["Свитеры и кофты"]] = treeLayer2[layer2["Свитеры и кофты"], layer2["Рубашки"]] = 0.8
treeLayer2[layer2["Рубашки"], layer2["Футболки"]] = treeLayer2[layer2["Футболки"], layer2["Рубашки"]] = 1
treeLayer2[layer2["Рубашки"], layer2["Лонгсливы"]] = treeLayer2[layer2["Лонгсливы"], layer2["Рубашки"]] = 1
treeLayer2[layer2["Рубашки"], layer2["Джинсы"]] = treeLayer2[layer2["Джинсы"], layer2["Рубашки"]] = 0.6
treeLayer2[layer2["Рубашки"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Рубашки"]] = 1

treeLayer2[layer2["Спортивные футболки"], layer2["Спортивные шорты"]] = treeLayer2[layer2["Спортивные шорты"], layer2["Спортивные футболки"]] = 0.3
treeLayer2[layer2["Спортивные футболки"], layer2["Спортивные брюки"]] = treeLayer2[layer2["Спортивные брюки"], layer2["Спортивные футболки"]] = 0.3
treeLayer2[layer2["Спортивные футболки"], layer2["Спортивные толстовки"]] = treeLayer2[layer2["Спортивные толстовки"], layer2["Спортивные футболки"]] = 0.2
treeLayer2[layer2["Спортивные футболки"], layer2["Свитеры и кофты"]] = treeLayer2[layer2["Свитеры и кофты"], layer2["Спортивные футболки"]] = 0.7
treeLayer2[layer2["Спортивные футболки"], layer2["Футболки"]] = treeLayer2[layer2["Футболки"], layer2["Спортивные футболки"]] = 0.2
treeLayer2[layer2["Спортивные футболки"], layer2["Лонгсливы"]] = treeLayer2[layer2["Лонгсливы"], layer2["Спортивные футболки"]] = 0.7
treeLayer2[layer2["Спортивные футболки"], layer2["Джинсы"]] = treeLayer2[layer2["Джинсы"], layer2["Спортивные футболки"]] = 0.6
treeLayer2[layer2["Спортивные футболки"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Спортивные футболки"]] = 0.5

treeLayer2[layer2["Спортивные шорты"], layer2["Спортивные брюки"]] = treeLayer2[layer2["Спортивные брюки"], layer2["Спортивные шорты"]] = 0.4
treeLayer2[layer2["Спортивные шорты"], layer2["Спортивные толстовки"]] = treeLayer2[layer2["Спортивные толстовки"], layer2["Спортивные шорты"]] = 0.5
treeLayer2[layer2["Спортивные шорты"], layer2["Свитеры и кофты"]] = treeLayer2[layer2["Свитеры и кофты"], layer2["Спортивные шорты"]] = 0.8
treeLayer2[layer2["Спортивные шорты"], layer2["Футболки"]] = treeLayer2[layer2["Футболки"], layer2["Спортивные шорты"]] = 0.4
treeLayer2[layer2["Спортивные шорты"], layer2["Лонгсливы"]] = treeLayer2[layer2["Лонгсливы"], layer2["Спортивные шорты"]] = 0.7
treeLayer2[layer2["Спортивные шорты"], layer2["Джинсы"]] = treeLayer2[layer2["Джинсы"], layer2["Спортивные шорты"]] = 1
treeLayer2[layer2["Спортивные шорты"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Спортивные шорты"]] = 0.4

treeLayer2[layer2["Спортивные брюки"], layer2["Спортивные толстовки"]] = treeLayer2[layer2["Спортивные толстовки"], layer2["Спортивные брюки"]] = 0.4
treeLayer2[layer2["Спортивные брюки"], layer2["Свитеры и кофты"]] = treeLayer2[layer2["Свитеры и кофты"], layer2["Спортивные брюки"]] = 0.7
treeLayer2[layer2["Спортивные брюки"], layer2["Футболки"]] = treeLayer2[layer2["Футболки"], layer2["Спортивные брюки"]] = 0.5
treeLayer2[layer2["Спортивные брюки"], layer2["Лонгсливы"]] = treeLayer2[layer2["Лонгсливы"], layer2["Спортивные брюки"]] = 0.9
treeLayer2[layer2["Спортивные брюки"], layer2["Джинсы"]] = treeLayer2[layer2["Джинсы"], layer2["Спортивные брюки"]] = 1
treeLayer2[layer2["Спортивные брюки"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Спортивные брюки"]] = 0.9

treeLayer2[layer2["Спортивные толстовки"], layer2["Свитеры и кофты"]] = treeLayer2[layer2["Свитеры и кофты"], layer2["Спортивные толстовки"]] = 0.5
treeLayer2[layer2["Спортивные толстовки"], layer2["Футболки"]] = treeLayer2[layer2["Футболки"], layer2["Спортивные толстовки"]] = 0.4
treeLayer2[layer2["Спортивные толстовки"], layer2["Лонгсливы"]] = treeLayer2[layer2["Лонгсливы"], layer2["Спортивные толстовки"]] = 0.6
treeLayer2[layer2["Спортивные толстовки"], layer2["Джинсы"]] = treeLayer2[layer2["Джинсы"], layer2["Спортивные толстовки"]] = 0.4
treeLayer2[layer2["Спортивные толстовки"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Спортивные толстовки"]] = 0.8

treeLayer2[layer2["Свитеры и кофты"], layer2["Футболки"]] = treeLayer2[layer2["Футболки"], layer2["Свитеры и кофты"]] = 0.7
treeLayer2[layer2["Свитеры и кофты"], layer2["Лонгсливы"]] = treeLayer2[layer2["Лонгсливы"], layer2["Свитеры и кофты"]] = 0.6
treeLayer2[layer2["Свитеры и кофты"], layer2["Джинсы"]] = treeLayer2[layer2["Джинсы"], layer2["Свитеры и кофты"]] = 0.5
treeLayer2[layer2["Свитеры и кофты"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Свитеры и кофты"]] = 1

treeLayer2[layer2["Футболки"], layer2["Лонгсливы"]] = treeLayer2[layer2["Лонгсливы"], layer2["Футболки"]] = 0.5
treeLayer2[layer2["Футболки"], layer2["Джинсы"]] = treeLayer2[layer2["Джинсы"], layer2["Футболки"]] = 0.5
treeLayer2[layer2["Футболки"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Футболки"]] = 0.5

treeLayer2[layer2["Лонгсливы"], layer2["Джинсы"]] = treeLayer2[layer2["Джинсы"], layer2["Лонгсливы"]] = 0.5
treeLayer2[layer2["Лонгсливы"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Лонгсливы"]] = 1

treeLayer2[layer2["Джинсы"], layer2["Шорты"]] = treeLayer2[layer2["Шорты"], layer2["Джинсы"]] = 1

layer3 = {
    "Рубашки с коротким рукавом": 0,
    "Рубашки с длинным рукавом": 1,
    "Спортивные классические брюки": 2,
    "Джоггеры": 3,
    "Тайцы": 4,
    "Свитшоты": 5,
    "Худи": 6,
    "Толстовки": 7,
}

treeLayer3 = np.zeros((len(layer3), len(layer3)))

treeLayer3[layer3["Рубашки с коротким рукавом"], layer3["Рубашки с длинным рукавом"]] = treeLayer3[layer3["Рубашки с длинным рукавом"], layer3["Рубашки с коротким рукавом"]] = 0.2
treeLayer3[layer3["Рубашки с коротким рукавом"], layer3["Спортивные классические брюки"]] = treeLayer3[layer3["Спортивные классические брюки"], layer3["Рубашки с коротким рукавом"]] = 1
treeLayer3[layer3["Рубашки с коротким рукавом"], layer3["Джоггеры"]] = treeLayer3[layer3["Джоггеры"], layer3["Рубашки с коротким рукавом"]] = 0.9
treeLayer3[layer3["Рубашки с коротким рукавом"], layer3["Тайцы"]] = treeLayer3[layer3["Тайцы"], layer3["Рубашки с коротким рукавом"]] = 1
treeLayer3[layer3["Рубашки с коротким рукавом"], layer3["Свитшоты"]] = treeLayer3[layer3["Свитшоты"], layer3["Рубашки с коротким рукавом"]] = 1
treeLayer3[layer3["Рубашки с коротким рукавом"], layer3["Худи"]] = treeLayer3[layer3["Худи"], layer3["Рубашки с коротким рукавом"]] = 1
treeLayer3[layer3["Рубашки с коротким рукавом"], layer3["Толстовки"]] = treeLayer3[layer3["Толстовки"], layer3["Рубашки с коротким рукавом"]] = 0.9

treeLayer3[layer3["Рубашки с длинным рукавом"], layer3["Спортивные классические брюки"]] = treeLayer3[layer3["Спортивные классические брюки"], layer3["Рубашки с длинным рукавом"]] = 1
treeLayer3[layer3["Рубашки с длинным рукавом"], layer3["Джоггеры"]] = treeLayer3[layer3["Джоггеры"], layer3["Рубашки с длинным рукавом"]] = 1
treeLayer3[layer3["Рубашки с длинным рукавом"], layer3["Тайцы"]] = treeLayer3[layer3["Тайцы"], layer3["Рубашки с длинным рукавом"]] = 1
treeLayer3[layer3["Рубашки с длинным рукавом"], layer3["Свитшоты"]] = treeLayer3[layer3["Свитшоты"], layer3["Рубашки с длинным рукавом"]] = 0.7
treeLayer3[layer3["Рубашки с длинным рукавом"], layer3["Худи"]] = treeLayer3[layer3["Худи"], layer3["Рубашки с длинным рукавом"]] = 1
treeLayer3[layer3["Рубашки с длинным рукавом"], layer3["Толстовки"]] = treeLayer3[layer3["Толстовки"], layer3["Рубашки с длинным рукавом"]] = 1

treeLayer3[layer3["Спортивные классические брюки"], layer3["Джоггеры"]] = treeLayer3[layer3["Джоггеры"], layer3["Спортивные классические брюки"]] = 0.6
treeLayer3[layer3["Спортивные классические брюки"], layer3["Тайцы"]] = treeLayer3[layer3["Тайцы"], layer3["Спортивные классические брюки"]] = 0.8
treeLayer3[layer3["Спортивные классические брюки"], layer3["Свитшоты"]] = treeLayer3[layer3["Свитшоты"], layer3["Спортивные классические брюки"]] = 0.8
treeLayer3[layer3["Спортивные классические брюки"], layer3["Худи"]] = treeLayer3[layer3["Худи"], layer3["Спортивные классические брюки"]] = 0.4
treeLayer3[layer3["Спортивные классические брюки"], layer3["Толстовки"]] = treeLayer3[layer3["Толстовки"], layer3["Спортивные классические брюки"]] = 0.4

treeLayer3[layer3["Джоггеры"], layer3["Тайцы"]] = treeLayer3[layer3["Тайцы"], layer3["Джоггеры"]] = 0.9
treeLayer3[layer3["Джоггеры"], layer3["Свитшоты"]] = treeLayer3[layer3["Свитшоты"], layer3["Джоггеры"]] = 0.6
treeLayer3[layer3["Джоггеры"], layer3["Худи"]] = treeLayer3[layer3["Худи"], layer3["Джоггеры"]] = 0.6
treeLayer3[layer3["Джоггеры"], layer3["Толстовки"]] = treeLayer3[layer3["Толстовки"], layer3["Джоггеры"]] = 0.5

treeLayer3[layer3["Тайцы"], layer3["Свитшоты"]] = treeLayer3[layer3["Свитшоты"], layer3["Тайцы"]] = 1
treeLayer3[layer3["Тайцы"], layer3["Худи"]] = treeLayer3[layer3["Худи"], layer3["Тайцы"]] = 0.8
treeLayer3[layer3["Тайцы"], layer3["Толстовки"]] = treeLayer3[layer3["Толстовки"], layer3["Тайцы"]] = 0.7

treeLayer3[layer3["Свитшоты"], layer3["Худи"]] = treeLayer3[layer3["Худи"], layer3["Свитшоты"]] = 0.3
treeLayer3[layer3["Свитшоты"], layer3["Толстовки"]] = treeLayer3[layer3["Толстовки"], layer3["Свитшоты"]] = 0.5

treeLayer3[layer3["Худи"], layer3["Толстовки"]] = treeLayer3[layer3["Толстовки"], layer3["Худи"]] = 0.3

layer = [layer1, layer2, layer3]
tree = [treeLayer1, treeLayer2, treeLayer3]


def getDataFrameStat(df):
    dfStat = df.copy()
    for elem in ["Цвет", "Бренд"]:
        del dfStat[elem]
    
    return dfStat


def _getDistance(v1, v2, nPow):
    res = 0
    for i in range(len(v1)):
        if isnan(v1[i]) or isnan(v2[i]):
            continue
        res += pow(abs(v1[i] - v2[i]), nPow)
        
    return pow(res, 1 / nPow)


# Манхэттенское расстояние
def getManhattanDistance(v1, v2):
    return _getDistance(v1, v2, 1)


# Евклидово расстояние
def getEuclideanDistance(v1, v2):
    return _getDistance(v1, v2, 2)


# Косинусное 
def getCos(v1, v2):
    v1T, v2T = v1.copy(), v2.copy()
    indArr = [i for i, (elem1, elem2) in enumerate(zip(v1T, v2T)) if isnan(elem1) or isnan(elem2)]
    v1T[:] = [elem for i, elem in enumerate(v1T) if i not in indArr]
    v2T[:] = [elem for i, elem in enumerate(v2T) if i not in indArr]

    return 1 - dot(v1T, v2T) / (norm(v1T) * norm(v2T))


# Расстояние по дереву
def getTreeDistance(v1, v2):
    res = 0
    size = max(len(v1), len(v2))

    for i in range(size):
        try:
            res += tree[i][layer[i][v1[i]]][layer[i][v2[i]]]
        except:
            res += 0.5
    
    return res / size


# Сравнение брендов
def getBrandDistance(v1, v2):
    return brandsMatr[brands[v1]][brands[v2]]


# Сравнение цветов
def getColorDistance(v1, v2):
    return colorsMatr[colors[v1]][colors[v2]]


# Найти все похожие
def getSimilarity(id, matr, nameArr):
    data = matr[id]
    res = pd.DataFrame(
        zip(data, nameArr), 
        index=np.arange(len(matr)), 
        columns=["Расстояние", "Название"]
    )
    return res.sort_values("Расстояние")


def calcDistance(f, df):
    matrData = df.values.tolist()
    n = len(matrData)
    matrRes = np.zeros((n, n))
    for i in range(n):
        for j in range(i, n):
            matrRes[i][j] = matrRes[j][i] = f(matrData[i], matrData[j])
            
    return matrRes / matrRes.max()   


def calcDistanceCompined(df, dfTree):
    dfTree = dfTree["Иерархия"]
    dfStatParams = getDataFrameStat(df)
    
    matrTree = calcDistance(getTreeDistance, dfTree)
    matrEucl = calcDistance(getEuclideanDistance, dfStatParams)
    # matrMan = calcDistance(getManhattanDistance, dfStatParams)
    # matrCos = calcDistance(getCos, dfStatParams)
    matrBrand = calcDistance(getBrandDistance, df["Бренд"])
    matrColor = calcDistance(getColorDistance, df["Цвет"])

    xTree = matrTree.max()
    xStat = matrEucl.max()
    # xStat = matrMan.max()
    # xStat = matrCos.max()
    xBrand = matrBrand.max()
    xColor = matrColor.max()

    kTree, kStat, kBrand, kColor = 4, 4, 1, 2

    return (kTree * matrTree + kStat * matrEucl + kBrand * matrBrand + kColor * matrColor) / \
        (kTree * xTree + kStat * xStat + kBrand * xBrand + kColor * xColor)


def draw(matrRes, nameArr, title, color='Inferno'):
    fig = px.imshow(matrRes, x=nameArr, y=nameArr, color_continuous_scale=color, title=title)
    fig.update_layout(width=1000, height=1200)
    fig.update_traces(text=nameArr)
    fig.update_xaxes(side="top")
    fig.show()


def drawManhattanDistance():
    matrRes = calcDistance(getManhattanDistance, getDataFrameStat(df))
    draw(matrRes, nameArr, "Манхэттенское расстояние")


def drawEuclideanDistance():
    matrRes = calcDistance(getEuclideanDistance, getDataFrameStat(df))
    draw(matrRes, nameArr, "Евклидово расстояние")


def drawCosDistance():
    matrRes = calcDistance(getCos, getDataFrameStat(df))
    draw(matrRes, nameArr, "Косинусная мера близости")


def drawBrandDistance():
    matrRes = calcDistance(getBrandDistance, df["Бренд"])
    draw(matrRes, nameArr, "Расстояние по брендам")


def drawColorDistance():
    matrRes = calcDistance(getColorDistance, df["Цвет"])
    draw(matrRes, nameArr, "Расстояние по цветам")


def drawTreeDistance():
    matrRes = calcDistance(getTreeDistance, dfTree["Иерархия"])
    draw(matrRes, nameArr, "Расстояние по дереву")


def drawCompinedDistance():
    draw(calcDistanceCompined(df, dfTree), nameArr, "Комбинированная мера")


#-----------------------------------------------------------------------------
#                                ЗАДАЧИ                                      #
#-----------------------------------------------------------------------------
    
matrSimilarity = calcDistanceCompined(df, dfTree)

def printRes(arr):
    print("\n%sРасстояние \t\t\t Название%s" %(GREEN, BASE))
    for elem in arr:
        for key, value in elem.items():
            print("{0}\t\t{1}".format(value, key))


# Задача 1
            
TASK_1_CONDITION = """
%sУсловие задачи%s

Вход: 1 объект (затравочный). 
Выход: список рекомендаций, ранжированный по убыванию близости с затравкой. 
    Примените Вашу обобщающую меру близости.
""" %(GREEN, BASE)
   

def _findSimilar(name):
    ind = df0[F_NAME].tolist().index(name)
    listSimilarity = getSimilarity(ind, matrSimilarity, nameArr)
    return listSimilarity


def findSimilar(name):
    listSimilarity = _findSimilar(name)
    return listSimilarity[listSimilarity[F_NAME] != name]


def task1():
    print(TASK_1_CONDITION)
    try:
        res = findSimilar(input("%sВведите затравочный объект:%s " %(GREEN, BASE))) 
    except:
        print("%s\nТакого объекта не существует%s" %(RED, BASE))
    else:
        print("\n", res)


# Задача 2

TASK_2_CONDITION = """
%sУсловие задачи%s

Вход: массив объектов (лайков). 
Выход: сформированный ранжированный список рекомендаций.
""" %(GREEN, BASE)


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
    return sorted(
        [{key: elem} for key, elem in resDict.items()], 
        key=lambda elem: list(elem.values())[0]
    )


def task2():
    print(TASK_2_CONDITION)
    try:
        res = findSimilarMany(input("%sВведите лайкнутые объекты, разделенные запятой:%s " %(GREEN, BASE)).split(","))
    except:
        print("%s\nНедопустимых формат ввода, либо таких объектов не существует%s" %(RED, BASE))
    else:
        printRes(res)


# Задача 3
        
TASK_3_CONDITION = """
%sУсловие задачи%s

Вход: массив затравочных объектов и массив дизлайков.
Выход: сформированный ранжированный список рекомендаций.
""" %(GREEN, BASE)


def delOpposite(dict, nameArr):
    for name in nameArr:
        if name in dict.keys():
            del dict[name]
    
    return dict


def findByReaction(likesArr=[], dislikesArr=[]):
    likesRec = delOpposite(_findSimilarMany(likesArr), dislikesArr)
    dislikesRec = delOpposite(_findSimilarMany(dislikesArr), likesArr)

    dictRes = {}
    if len(likesArr) == 0:
        for key, elem in dislikesRec.items():
            dictRes[key] = 1 - elem
        return sorted(
            [{key: elem} for key, elem in dictRes.items()], 
            key=lambda elem: list(elem.values())[0]
        )

    for key in likesRec.keys():
        if likesRec[key] <= dislikesRec[key]:
            dictRes[key] = likesRec[key]

    return sorted(
        [{key: elem} for key, elem in dictRes.items()], 
        key=lambda elem: list(elem.values())[0]
    )


def task3():
    print(TASK_3_CONDITION)
    try:
        likesArr = input("%sВведите лайкнутые объекты, разделенные запятой:%s " %(GREEN, BASE)).split(",")
        dislikesArr=input("%sВведите дизлайкнутые объекты, разделенные запятой:%s " %(GREEN, BASE)).split(",")

        for arr in [likesArr, dislikesArr]:
            while "" in arr:
                arr.remove("")

        res = findByReaction(
            likesArr=likesArr,
            dislikesArr=dislikesArr,
        )
    except:
        print("%s\nНедопустимых формат ввода, либо таких объектов не существует%s" %(RED, BASE))
    else:
        printRes(res)


#-----------------------------------------------------------------------------

def sortDict(resDict):
    sorted_tuples = sorted(resDict.items(), key=lambda item: item[1], reverse=False)
    sorted_dict = {k: v for k, v in sorted_tuples}

    return sorted_dict


def getArrFromSeries(data):
    arr = []
    for elem in data:
        arr.append(elem)

    return arr


namesUI = getArrFromSeries(nameArr)


def _fromArrDictToDict(arrDict):
    resDict = {}
    for elem in arrDict:
        resDict.update(elem)

    return resDict


def _compareLikesParams(likesDict, paramsDict):
    resDict = {}
    for key, value in likesDict.items():
        if key in paramsDict.keys():
            resDict[key] = value * paramsDict[key]
            del paramsDict[key]
        else:
            resDict[key] = value

    for key, value in paramsDict.items():
        resDict[key] = value

    return resDict


def _getDefaultResultParams(nameArr):
    resDict = {}
    for name in nameArr:
        resDict[name] = 0

    return resDict


def _getRecommendationParams(
    brandsSelected, 
    colorsSelected,
    sizesSelected,
    sexSelected,
    costlinessSelected, 
    categoriesSelected, 
    df
):
    dfColumnsArr = df.columns.values.tolist()
    indexDict = {}
    indexDict[dfColumnsArr.index('Пол')] = sexSelected
    indexDict[dfColumnsArr.index('Цвет')] = colorsSelected
    indexDict[dfColumnsArr.index('Размер')] = sizesSelected
    indexDict[dfColumnsArr.index('Бренд')] = brandsSelected

    for category in categoriesSelected:
        indexDict[dfColumnsArr.index(category)] = [1]

    for costliness in costlinessSelected:
        indexDict[dfColumnsArr.index(costliness)] = [1]

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
        if value != 0:
            resDict[nameArr[key]] = 1 - value / n

    return sortDict(resDict)


def getRecommendationParams(
    brandsSelected, 
    colorsSelected, 
    sizesSelected,
    sexSelected,
    costlinessSelected,
    categoriesSelected, 
    df
):
    nAll = 0
    if len(brandsSelected):
        nAll += 1
    if len(colorsSelected):
        nAll += 1
    if len(sizesSelected):
        nAll += 1
    if len(sexSelected):
        nAll += 1

    nAll += len(categoriesSelected) + len(costlinessSelected)
    if nAll == 0:
        recDict = _getDefaultResultParams(namesUI)
    else:
        recDict = _getRecommendationParams(
            brandsSelected=brandsSelected, 
            colorsSelected=colorsSelected, 
            sizesSelected=sizesSelected,
            sexSelected=sexSelected,
            costlinessSelected=costlinessSelected,
            categoriesSelected=categoriesSelected, 
            df=df
        )

    return _updateResult(recDict, nameArr, nAll)


def _getRecommendationArr(likesArr, dislikesArr):
    recArr = None
    if len(likesArr) and len(dislikesArr):
        recArr = findByReaction(likesArr, dislikesArr)
    elif len(likesArr) and len(dislikesArr) == 0:
        recArr = findSimilarMany(likesArr)
    elif len(likesArr) == 0 and len(dislikesArr):
        recArr = findByReaction(likesArr, dislikesArr)
    else:
        recArr = []

    return recArr


def _splitMustMaybeDictArr(recDict):
    recMust, recMaybe = [], []
    for name, value in recDict.items():
        if value <= 0.2:
            recMust.append(name)
        else:
            recMaybe.append(name)

    return recMust, recMaybe


def giveRecommendationFull(
    brandsSelected, 
    colorsSelected, 
    sizesSelected,
    sexSelected,
    costlinessSelected,
    categoriesSelected, 
    likesSelected, 
    dislikesSelected, 
    df
):
    recDict = getRecommendationParams(
        brandsSelected=brandsSelected, 
        colorsSelected=colorsSelected, 
        sizesSelected=sizesSelected,
        sexSelected=sexSelected,
        costlinessSelected=costlinessSelected,
        categoriesSelected=categoriesSelected,
        df=df
    )

    if len(likesSelected) or len(dislikesSelected):
        recLikesArr = _getRecommendationArr(likesSelected, dislikesSelected)
        recLikesDict = _fromArrDictToDict(recLikesArr)
        recDict = _compareLikesParams(recLikesDict, recDict)

    return _splitMustMaybeDictArr(sortDict(recDict))
