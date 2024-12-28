from turtle import onclick, width
import panel as pn
from func import *
import ipywidgets as widgets
from tkinter import font

def getArrFromSeries(data):
    arr = []
    for elem in data:
        arr.append(elem)
    return arr

def getDataFrameFromArr(data, reverse=1, must = 0):
    resArr = []
    if must:
        recommentlist.clear()
        valuelist.clear()
    for elem in data:
        for key in elem.keys():
            resArr.append({"Название": key, "Величина схожести": abs(reverse - elem[key])})
            if must:
                recommentlist.append(key)
                valuelist.append(abs(reverse - elem[key]))
    return pd.DataFrame(resArr, index=range(1, len(resArr) + 1), columns=["Название", "Величина схожести"])

def _initMustTable(recArr, reverse = 1, must = 1):
    tableRecMust.value = getDataFrameFromArr(recArr, reverse, must)
    
    markdownResultMustTitle.visible = True
    tableRecMust.visible = True


def _initMaybeTable(recArr):
    tableRecMaybe.value = getDataFrameFromArr(recArr)
    
    markdownResultMaybeTitle.visible = True
    tableRecMaybe.visible = True


def _changeStatusError(isError):
    if isError:
        markdownError.visible = True
        markdownDefault.visible = False
        markdownResultMustTitle.visible = False
        markdownResultMaybeTitle.visible = False

        tableRecMust.visible = False
        tableRecMaybe.visible = False
    else:
        markdownError.visible = False
        markdownDefault.visible = True

def _splitMustMaybe(recArr, filter = []):
    recMust, recMaybe = [], []
    for rec in recArr:
        for key in rec.keys():
            if key not in filter:
                continue
            if rec[key] <= 0.5:
                recMust.append(rec)
            else:
                recMaybe.append(rec)
    return recMust, recMaybe

def _isRightInput(arr1, arr2):
    inner = list(set(arr1) & set(arr2))
    return len(inner) == 0

def _getDefaultResult(nameArr):
    resArr = []
    for name in nameArr:
        resArr.append({name: 1})
    return resArr

def _getRecommendationArr(likesArr, dislikesArr):
    recArr = None

    if len(likesArr) and len(dislikesArr):
        recArr = findSimilar3(likesArr, dislikesArr, df0, nameArr, matrSimilarity)
    elif len(likesArr) and len(dislikesArr) == 0:
        recArr = findSimilarMany(likesArr, df0, nameArr, matrSimilarity)
    elif len(likesArr) == 0 and len(dislikesArr):
        recArr = findSimilar3(likesArr, dislikesArr, df0, nameArr, matrSimilarity)
    else:
        recArr = _getDefaultResult(namesUI)
    return recArr

def _giveRecommendation(likesArr, dislikesArr, filter = []):
    recArr = _getRecommendationArr(likesArr, dislikesArr)

    recMust, recMaybe = _splitMustMaybe(recArr, filter)

    _initMustTable(recMust, must = 1)
    _initMaybeTable(recMaybe)

def run(a):
    likesArr = choiceLiked.value
    dislikesArr = choiceDisliked.value

    if not _isRightInput(likesArr, dislikesArr):
        _changeStatusError(isError=True)
        return
    _changeStatusError(isError=False)
    sexSelected = sexWidget.value
    countrySelected = countryWidget.value
    brandSelected = brandWidget.value
    conSelected = conWidget.value
    sexSelected = _updateSex(sexSelected)
    conSelected = _updateCon(conSelected)
    nAll = 0
    if len(sexSelected):
        nAll += 1
    if len(countrySelected):
        nAll += 1
    if len(brandSelected):
        nAll += 1
    if len(conSelected):
        nAll += 1
    dfColumnsArr = df.columns.values.tolist()
    indexDict = {}
    indexDict[dfColumnsArr.index('Пол')] = sexSelected
    indexDict[dfColumnsArr.index('Бренд')] = brandSelected
    indexDict[dfColumnsArr.index('Страна')] = countrySelected
    indexDict[dfColumnsArr.index('Концентрация')] = conSelected
    res = []
    matrData = df.values.tolist()
    for i in range(len(matrData)):
        s = 0
        for ind in indexDict.keys():
            if matrData[i][ind] in indexDict[ind]:
                s += 1
        if s == nAll:
            res.append(nameArr[i])
    _giveRecommendation(likesArr, dislikesArr, filterList)

def _updateSex(sexArr):
    res = []
    for sex in sexArr:
        res.append(sexDict[sex[0]])
    return res
def _updateCon(conArr):
    res = []
    for con in conArr:
        res.append(conDict[con])
    return res

def search(a):
    sexSelected = sexWidget.value
    countrySelected = countryWidget.value
    brandSelected = brandWidget.value
    conSelected = conWidget.value
    sexSelected = _updateSex(sexSelected)
    conSelected = _updateCon(conSelected)
    nAll = 0
    if len(sexSelected):
        nAll += 1
    if len(countrySelected):
        nAll += 1
    if len(brandSelected):
        nAll += 1
    if len(conSelected):
        nAll += 1
    if not nAll:
        pass
    global filterList, valueFlist
    dfColumnsArr = df.columns.values.tolist()
    indexDict = {}
    indexDict[dfColumnsArr.index('Пол')] = sexSelected
    indexDict[dfColumnsArr.index('Бренд')] = brandSelected
    indexDict[dfColumnsArr.index('Страна')] = countrySelected
    indexDict[dfColumnsArr.index('Концентрация')] = conSelected
    res = []
    matrData = df.values.tolist()
    for i in range(len(matrData)):
        s = 0
        for ind in indexDict.keys():
            if matrData[i][ind] in indexDict[ind]:
                s += 1
        if s == nAll:
            res.append(nameArr[i])
    if not len(res):
        _initMustTable([])
    filtered_name = [recommentlist[i] for i in range(len(recommentlist)) if recommentlist[i] in res]  
    filtered_value = [valuelist[i] for i in range(len(recommentlist)) if recommentlist[i] in res]  
    recMust = [{k: v} for k, v in zip(filtered_name, filtered_value)]
    _initMustTable(recMust, 0, 0)
    filterList = [x for x in filtered_name]
    valueFlist = [x for x in filtered_value]

def reset(b):
    global recommentlist, valueFlist, valuelist, filterList
    recommentlist.clear()
    valuelist.clear()
    filterList.clear()
    valueFlist.clear()
    recommentlist = getArrFromSeries(nameArr)
    valuelist = [1 for x in recommentlist]
    filterList = getArrFromSeries(nameArr)
    valueFlist = [1 for x in filterList]
    tableRecMaybe.visible = False
    tableRecMust.visible = False
    markdownResultMustTitle.visible = False
    markdownResultMaybeTitle.visible = False

df0, df, dfTree, nameArr, itemSmells, smellLike  = preprocessing()
matrSimilarity = calcDistanceCompined(df, dfTree, nameArr)
pn.extension()
namesUI = getArrFromSeries(nameArr)
recommentlist = getArrFromSeries(nameArr)
valuelist = [1 for x in recommentlist]
filterList = getArrFromSeries(nameArr)
valueFlist = [1 for x in filterList]
sexDict = { "м": 0, "ж": 1 }
conDict = {"освежающая вода": 0, "одеколон": 0.2, "туалетная вода": 0.4, "парфюмерная вода": 0.6, "духи": 0.8, "масляные духи": 1}
choiceLiked = pn.widgets.MultiChoice(
    name='Мне нравится', 
    value=[],
    width=320,
    options=namesUI)

choiceDisliked = pn.widgets.MultiChoice(
    name='Мне не нравится', 
    value=[],
    width=320,
    options=namesUI)

markdownError = pn.pane.Markdown('### Ошибка ввода', width=800, visible=False)
markdownDefault = pn.pane.Markdown("# Выберете то, что: ", width=800, visible=True)
markdownResultMustTitle = pn.pane.Markdown("#### Попробуйте следующие ароматы: ", width=300, visible=False)
markdownResultMaybeTitle = pn.pane.Markdown("#### Возможно Вам понравятся: ", width=300, visible=False)

bokeh_formatters = {
    "Величина схожести": {'type': 'progress', 'max': 1}
}

tableRecMust = pn.widgets.Tabulator(visible=False, formatters=bokeh_formatters)
tableRecMaybe = pn.widgets.Tabulator(visible=False, formatters=bokeh_formatters)
button = pn.widgets.Button(
    name='Рекомендовать',
    button_type='success',
    width=50,
    height=40,
    margin=(24, 100, 10, 10))
button.on_click(run)

recomment = pn.Column(
    markdownDefault,
    markdownError,
    pn.Row(
        pn.Column(choiceLiked, height=100),
        pn.Column(choiceDisliked, height=100)
    ),
    button,
    pn.Column(markdownResultMustTitle, 
        tableRecMust,
        markdownResultMaybeTitle, 
        tableRecMaybe)
)

sexWidget = pn.widgets.CheckBoxGroup(
    name='Пол', 
    options=['мужской', 'женский'],
    inline=False
)
sexElem = pn.Card(
    sexWidget, 
    title='Пол',
    width=400,
    margin=(10, 30, 10, 10))

countryArr = list(set(df0['Страна'].tolist()))

countryWidget = pn.widgets.MultiChoice(
    value=[],
    options=countryArr)
countryElem = pn.Card(
    countryWidget,
    title='Страна-производитель',
    width=400,
    margin=(10, 30, 10, 10))

brandArr = list(set(df0['Бренд'].tolist()))

brandWidget = pn.widgets.MultiChoice(
    value=[],
    options=brandArr)
brandElem = pn.Card(
    brandWidget,
    title='Бренд',
    width=400,
    margin=(10, 30, 10, 10))

conArr = list(set(df0['Концентрация'].tolist()))

conWidget = pn.widgets.MultiChoice(
    value=[],
    options=conArr)
conElem = pn.Card(
    conWidget,
    title='Концентрация',
    width=400,
    margin=(10, 30, 10, 10))

buttonFilter = pn.widgets.Button(
    name='Фильтр',
    button_type='success',
    width=50,
    height=40,
    margin=(24, 100, 10, 10))
buttonFilter.on_click(search)

resetButton = pn.widgets.Button(
    name='Reset',
    button_type='success',
    width=50,
    height=40,
    margin=(24, 100, 10, 10))
resetButton.on_click(reset)

filter = pn.Column(
    pn.Row(sexElem, countryElem), 
    pn.Row(brandElem, conElem),
    pn.Row(buttonFilter,resetButton)
)

pLikes = pn.Row(
    recomment,
    filter
)
pn.serve(pLikes)

