from color import *
from recSystem import (
    drawManhattanDistance,
    drawEuclideanDistance,
    drawCosDistance,
    drawBrandDistance,
    drawColorDistance,
    drawTreeDistance,
    drawCompinedDistance,
    task1,
    task2,
    task3
)


MSG = """
    \t%sМеню\n
    1.  Манхэттенское расстояние;
    2.  Евклидово расстояние;
    3.  Косинусное расстояние;
    4.  Расстояние по брендам;
    5.  Расстояние по цветам;
    6.  Расстояние по дереву;
    7.  Комбинированное расстояние;

    8.  Задача 1;
    9.  Задача 2;
    10. Задача 3;

    0.  Выход.\n
    %sВыбор: %s""" %(YELLOW, GREEN, BASE)


def inputOption():
    try:
        option = int(input(MSG))
    except:
        option = -1
    
    if option < 0 or option > 10:
        print("%s\nОжидался ввод целого числа от 0 до 10%s" %(RED, BASE))

    return option


def main():
    option = -1
    while option != 0:
        option = inputOption()
        match option:
            case 1:
                drawManhattanDistance()
            case 2:
                drawEuclideanDistance()
            case 3:
                drawCosDistance()
            case 4:
                drawBrandDistance()
            case 5:
                drawColorDistance()
            case 6:
                drawTreeDistance()
            case 7:
                drawCompinedDistance()
            case 8:
                task1()
            case 9:
                task2()
            case 10:
                task3()
        

if __name__ == "__main__":
    main()
