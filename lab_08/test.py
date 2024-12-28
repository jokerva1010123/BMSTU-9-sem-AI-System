import re

from preprocessing import preprocessing
from question import *

userInputDict = {
    # Вопрос 1
    'что можете предложить?': WHAT_EXISTS,
    'что есть в наличие': WHAT_EXISTS,
    'что у вас есть в наличие': WHAT_EXISTS,
    'что у вас есть': WHAT_EXISTS,
    'какой у вас есть парфюм в наличии?': WHAT_EXISTS,
    'какой у вас парфюм есть в наличии?': WHAT_EXISTS,
    'какой у вас есть парфюм?': WHAT_EXISTS,
    # Вопрос 2
    'какие у вас есть духи?': WHAT_EXISTS_KINDPARFUM,
    'что есть из туалетной воды': WHAT_EXISTS_KINDPARFUM,
    # Вопрос 3
    'я не совсем знаю, что надо': SHOW_ANY,
    'помогите мне, пожалуйста, я совсем ничего не знаю': SHOW_ANY,
    # Вопрос 4
    'хочется свежий аромат': WANT_ABSTRACT,
    'хочу свежую парфюмерную воду': WANT_ABSTRACT,
    'мне очень нужен сладкий запах': WANT_ABSTRACT,
    'есть свежий масляные духи?': WANT_ABSTRACT,
    # Вопрос 5
    'хочется чего-то с запахом бергамота': WANT_ABSTRACT_OBJ,
    'хочу аромат, который пахнет густым дымом': WANT_ABSTRACT_OBJ_KINDPARFUM,

    'мне нравится томный аромат': I_LIKE_TAG,
    'обожаю лаванда': I_LIKE_OBJ,
    # Вопрос 6
    'нужен аромат похожий на Shalimar': SIMILAR_TO_BRAND,
    'хочу купить аналог парфюма Infinite Definitive': SIMILAR_TO_BRAND,

    'нужен аромат не похожий на Shalimar': NOT_SIMILAR_TO_BRAND,
    # Вопрос 8
    'мне нравятся французские духи': COUNTRY_EXT_KINDPARFUM_1,
    'я бы хотела купить туалетную воду из Германии': COUNTRY_EXT_KINDPARFUM_2,

    'хочу аромат средней стойкости': SHOW_DURABILITY,
    'нужны духи высокой стойкости': SHOW_DURABILITY,
    'а есть что-нибудь высокой стойкости': SHOW_DURABILITY
}

def run():
    for userInput, ruleRes in userInputDict.items():
        userProcessed = preprocessing(userInput)
        print(">>> ", userProcessed)

        for rule in RULE_ARR:
            regexp = re.compile(rule)
            match = regexp.match(userProcessed)
            if match != None:
                res = match.groupdict()
                print('MATCHED: ', rule == ruleRes)
                print('RULE: ', rule)
                print('RESULT: {}\n'.format(res))


if __name__ == "__main__":
    run()