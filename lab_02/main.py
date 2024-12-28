from preprocessing import *
from measures import *

df, dfTree, nameArr  = preprocessing()

matrRes = calcDistance(getManhattanDistance, getDataFrameAroma(df))
draw(matrRes, nameArr, "Манхэттенское расстояние")

matrRes = calcDistance(getEuclideanDistance, getDataFrameStat(df))
draw(matrRes, nameArr, "Евклидово расстояние")

matrRes = calcDistance(getBrandDistance, df["Бренд"])
draw(matrRes, nameArr, "Расстояние по брендам")

matrRes = calcDistance(getCountryDistance, df["Страна"])
draw(matrRes, nameArr, "Расстояние по парфюмерным школам")

matrRes = calcDistance(getCos, getDataFrameAroma(df))
draw(matrRes, nameArr, "Косинусное подобие")

tempDF = getDataFrameAroma(df)
del tempDF["Шлейф"]

matrRes = getJacquard(tempDF)
draw(matrRes, nameArr, "Мера Жаккара")

matrRes = calcDistance(getTreeDistance, dfTree["Семейства"])
draw(matrRes, nameArr, "Расстояние по дереву")

draw(calcDistanceCompined(df, dfTree, nameArr), nameArr, "Комбинированная мера")