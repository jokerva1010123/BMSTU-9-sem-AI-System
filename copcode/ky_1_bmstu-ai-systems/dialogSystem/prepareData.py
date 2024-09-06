from data import namesUI, giveRecommendationFull, df
from preprocessing import getNormalFormPhrase


def initPrefer():
    return {
        "likes": [], 
        "dislikes": [], 
        "brands": [], 
        "colors": [],
        "sizes": [],
        "sex": [],
        "costliness": [],
        "categories": [],
    }


def resetPrefer(dictPrefer):
    for key in dictPrefer.keys():
        dictPrefer[key] = []
        
    return dictPrefer


def _replaceNames(inputArr):
    namesArr = []
    namesDict = {}
    for i in range(len(namesUI)):
        namesDict[getNormalFormPhrase(namesUI[i].lower()).replace(" & ", "&").replace(" '", "\\'")] = i

    for name in inputArr:
        if name in namesDict.keys():
            if namesUI[namesDict[name]] not in namesArr:
                namesArr.append(namesUI[namesDict[name]])
        else:
            namesArr.append(name)

    return namesArr


def _replaceBrands(inputArr):
    brandsArr = []
    brandsDict = {
        "briony": "Briony",
        "Corneliani": "Corneliani",
        "hugo boss": "Hugo Boss",
        "canali": "Canali",
        "h&m": "H&M",
        "zara": "Zara",
        "levi's": "Levi's",
        "levis": "Levi's",
        "lacoste": "Lacoste",
        "nike": "Nike",
        "adidas": "Adidas",
        "puma": "Puma",
        "reebok": "Reebok",
    }

    for brand in inputArr:
        if brand not in brandsDict.values() and \
            brand in brandsDict.keys():
            if brandsDict[brand] not in brandsArr:
                brandsArr.append(brandsDict[brand])
        else:
            brandsArr.append(brand)

    return brandsArr


def _replaceColors(inputArr):
    colorsArr = []
    colorsDict = {
        "белый": "Белый",
        "чёрный": "Черный",
        "серый": "Серый",
        "синий": "Синий",
        "голубой": "Голубой",
        "красный": "Красный",
        "розовый": "Розовый",
    }
    
    for color in inputArr:
        if color not in colorsDict.values() and \
            color in colorsDict.keys():
            if colorsDict[color] not in colorsArr:
                colorsArr.append(colorsDict[color])
        else:
            colorsArr.append(color)

    return colorsArr


def _replaceCategories(inputArr):
    categoriesArr = []
    categoriesDict = {
        "пиджак": "Пиджаки",
        "брюк": "Брюки",
        "рубашка с короткий рукав": "Рубашки с коротким рукавом",
        "рубашка с длинный рукав": "Рубашки с длинным рукавом",
        "спортивный футболка": "Спортивные футболки",
        "спортивный шорты": "Спортивные шорты",
        "спортивный классический штаны": "Спортивные классические брюки",
        "джоггер": "Джоггеры",
        "таец": "Тайцы",
        "спортивный толстовка": "Спортивные толстовки",
        "свитшота": "Свитшоты",
        "худить": "Худи",
        "толстовка": "Толстовки",
        "футболка": "Футболки",
        "лонгслить": "Лонгсливы",
        "джинса": "Джинсы",
        "шорты": "Шорты",
        "рубашка": "Рубашки",
        "спортивный штаны": "Спортивные брюки",
        "свитер и кофта": "Свитеры и кофты",
        "деловой одежда": "Деловая одежда",
        "спортивный одежда": "Спортивная одежда",
        "повседневный одежда": "Повседневная одежда",
    }
    
    for category in inputArr:
        if category not in categoriesDict.values() and \
            category in categoriesDict.keys():
            if categoriesDict[category] not in categoriesArr:
                categoriesArr.append(categoriesDict[category])
        else:
            categoriesArr.append(category)

    return categoriesArr


def find(paramDict):
    paramDict["likes"] = _replaceNames(paramDict["likes"])
    paramDict["dislikes"] = _replaceNames(paramDict["dislikes"])
    paramDict["brands"] = _replaceBrands(paramDict["brands"])
    paramDict["colors"] = _replaceColors(paramDict["colors"])
    paramDict["categories"] = _replaceCategories(paramDict["categories"])
    paramDict["sizes"] = list(dict.fromkeys(paramDict["sizes"]))
    paramDict["sex"] = list(dict.fromkeys(paramDict["sex"]))
                              
    return giveRecommendationFull(
        brandsSelected=paramDict["brands"], 
        colorsSelected=paramDict["colors"], 
        sizesSelected=paramDict["sizes"],
        sexSelected=paramDict["sex"],
        costlinessSelected=paramDict["costliness"],
        categoriesSelected=paramDict["categories"], 
        likesSelected=paramDict["likes"], 
        dislikesSelected=paramDict["dislikes"],
        df=df
    )
