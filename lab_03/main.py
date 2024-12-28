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

def getDataFrameFromArr(data, reverse=0):
    resArr = []
    for elem in data:
        for key in elem.keys():
            resArr.append({"Название": key, "Величина схожести": 1 - elem[key] + reverse * (2 * elem[key] - 1)})
            
    return pd.DataFrame(resArr, index=range(1, len(resArr) + 1), columns=["Название", "Величина схожести"])

def _initMustTable(recArr):
    tableRecMust.value = getDataFrameFromArr(recArr)
    
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

def _splitMustMaybe(recArr):
    recMust, recMaybe = [], []
    for rec in recArr:
        for key in rec.keys():
            if rec[key] <= 0.5:
                recMust.append(rec)
            else:
                recMaybe.append(rec)
    return recMust, recMaybe

def _splitMustMaybeDict(recDict):
    recMust, recMaybe = [], []
    for name, value in recDict.items():
        if value >= 0.5:
            recMust.append({name: value})
        else:
            recMaybe.append({name: value})
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

def _giveRecommendation(likesArr, dislikesArr):
    recArr = _getRecommendationArr(likesArr, dislikesArr)

    recMust, recMaybe = _splitMustMaybe(recArr)

    _initMustTable(recMust)
    _initMaybeTable(recMaybe)


def run(a):
    likesArr = choiceLiked.value
    dislikesArr = choiceDisliked.value

    if not _isRightInput(likesArr, dislikesArr):
        _changeStatusError(isError=True)
        return

    _changeStatusError(isError=False)
    _giveRecommendation(likesArr, dislikesArr)

df0, df, dfTree, nameArr, itemSmells, smellLike  = preprocessing()
matrSimilarity = calcDistanceCompined(df, dfTree, nameArr)
pn.extension()
namesUI = getArrFromSeries(nameArr)

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
markdownDefault = pn.pane.Markdown("#### Выберете то, что: ", width=800, visible=True)
markdownResultMustTitle = pn.pane.Markdown("#### Попробуйте следующие ароматы: ", width=300, visible=False)
markdownResultMaybeTitle = pn.pane.Markdown("#### Возможно Вам понравятся: ", width=300, visible=False)

bokeh_formatters = {
    "Величина схожести": {'type': 'progress', 'max': 1}
}

tableRecMust = pn.widgets.Tabulator(visible=False, formatters=bokeh_formatters)
tableRecMaybe = pn.widgets.Tabulator(visible=False, formatters=bokeh_formatters)
button = pn.widgets.Button(
    name='Готово',
    button_type='success',
    width=50,
    height=40,
    margin=(24, 100, 10, 10))
button.on_click(run)

pLikes = pn.Column(
    markdownDefault,
    markdownError,
    pn.Row(
        pn.Column(choiceLiked, height=800),
        pn.Column(choiceDisliked, height=800),
        button,
        pn.Column(markdownResultMustTitle, 
            tableRecMust,
            markdownResultMaybeTitle, 
            tableRecMaybe))
)
pn.serve(pLikes)
