NAME = r'(?P<name>(спортивный классический брюки adidas|брюки corneliani|спортивный классический брюки nike|пиджак briony|джинсы levi\'s|шорты levi\'s|таец reebok|толстовка zara|рубашка с короткий рукав hugo boss|спортивный классический брюки reebok|брюки briony|спортивный шорты reebok|спортивный футболка puma|спортивный толстовка adidas|свитшота h&m|спортивный толстовка puma|спортивный классический брюки puma|толстовка levi\'s|худить zara|шорты h&m|спортивный шорты adidas|рубашка с длинный рукав hugo boss|спортивный толстовка nike|джоггера reebok|рубашка с длинный рукав briony|рубашка с короткий рукав briony|спортивный шорты puma|футболка lacoste|лонгслить h&m|футболка h&m|брюки hugo boss|таец adidas|таец nike|джинсы lacoste|худить lacoste|пиджак hugo boss|джинсы h&m|рубашка с короткий рукав corneliani|спортивный футболка nike|лонгслить zara|худить h&m|пиджак corneliani|футболка zara|толстовка h&m|шорты zara|спортивный футболка adidas|джоггера puma|лонгслить lacoste|спортивный шорты nike|шорты lacoste|свитшота lacoste|спортивный футболка reebok|толстовка lacoste|лонгслить levi\'s|джоггера adidas|свитшота levi\'s|пиджак canali|брюки canali|футболка levi\'s|джоггера nike|джинсы zara|худить levi\'s|рубашка с длинный рукав corneliani|рубашка с короткий рукав canali|спортивный толстовка reebok|свитшота zara|таец puma|рубашка с длинный рукав canali))'
CATEGORIES = r'(?P<category>(спортивный классический штаны|спортивный штаны|брюк|пиджак|рубашка с короткий рукав|рубашка с длинный рукав|спортивный футболка|спортивный шорты|джоггер|таец|спортивный толстовка|свитшота|худить|толстовка|футболка|лонгслить|джинса|шорты|рубашка|свитер и кофта|деловой одежда|спортивный одежда|повседневный одежда))'
BRAND = r'(?P<brand>(briony|corneliani|hugo boss|canali|h&m|zara|levi\'s|levis|lacoste|nike|adidas|puma|reebok))'
COLOR = r'(?P<color>(белый|чёрный|серый|синий|голубой|красный|розовый))'
SIZE = r'(?P<size>(42|44|46|48|50|s|m|xxl|xl|l))'
SEX = r'(?P<sex>(мужской|женский|девушка|женищина|мужчина|парень))'

WANT = r'(?P<want>(хотеться|хотеть|нужно|нужный|надо|искать|есть|быть|предпочитать|выбирать|выбрать|дать|посмотреть))'
LIKE = r'(?P<like>(нравиться|обожать|любить|фанат))'
DISLIKE = r'(?P<dislike>(не переносить|не нравиться|не подходить|не любить|терпеть не мочь|ненавидеть))'

SIMILAR_TO = r'(?P<similar_to>(похожий|на подобие|аналог|тип))'
NOT_SIMILAR_TO = r'(?P<not_similar_to>(не похожий|отличный от))'

LIKE_EXT = r'({}|{})'.format(LIKE, SIMILAR_TO)
DISLIKE_EXT = r'({}|{})'.format(DISLIKE, NOT_SIMILAR_TO)
WANT_EXT = r'({}|{})'.format(WANT, LIKE)

VERY = r'(очень|самый|супер|максимальный)'
LOW_COST = r'(дешёвый|низкий стоимость)'
AVERAGE_COST = r'(нормальный стоимость|средний стоимость|обычный стоимость|недорогой)'
HIGH_COST = r'(дорогой|высокий стоимость)'

SIMILAR_TO_NAME = r'.*{}.*?{}.*'.format(LIKE_EXT, NAME)
NOT_SIMILAR_TO_NAME = r'.*{}.*?{}.*'.format(DISLIKE_EXT, NAME)

WANT_CATEGORY = r'.*{}.*?{}.*'.format(WANT_EXT, CATEGORIES)
WANT_BRAND = r'.*{}.*{}.*'.format(WANT_EXT, BRAND)
WANT_COLOR = r'.*{}.*{}.*'.format(WANT_EXT, COLOR)
WANT_SIZE_BEFORE = r'.*{}.*размер {}.*'.format(WANT, SIZE)
WANT_SIZE_AFTER = r'.*{}.*{} размер.*'.format(WANT, SIZE)
WANT_SEX = r'.*{}.*{}.*'.format(WANT, SEX)
WANT_VERY_LOW_COST = r'.*{}.*{}.*{}.*'.format(WANT_EXT, VERY, LOW_COST)
WANT_LOW_COST = r'.*{}.*{}.*'.format(WANT_EXT, LOW_COST)
WANT_AVERAGE_COST = r'.*{}.*{}.*'.format(WANT_EXT, AVERAGE_COST)
WANT_HIGH_COST = r'.*{}.*{}.*'.format(WANT_EXT, HIGH_COST)
WANT_VERY_HIGH_COST = r'.*{}.*{}.*{}.*'.format(WANT_EXT, VERY, HIGH_COST)

HELP = r'(посоветовать|помочь|предложить|подсказать|показать|порекомендовать|посмотреть|ознакомиться)'
NOT_KNOW_GENERAL = r'((не.*знать).*(хотеть|надо))'

GENERAL_QUESTION = r'что|какой'
EXIST = r'есть|в наличие|в продажа|купить|выбрать|предложить|представить'

SHOW_ANY = r'.*({}|{}).*'.format(HELP, NOT_KNOW_GENERAL)
WHAT_EXISTS = r'.*{}.*{}.*'.format(GENERAL_QUESTION, EXIST)

RULE_ARR = [
    NOT_SIMILAR_TO_NAME,
    SIMILAR_TO_NAME,
    WANT_CATEGORY,
    WANT_BRAND,
    WANT_COLOR,
    WANT_SIZE_BEFORE,
    WANT_SIZE_AFTER,
    WANT_SEX,
    WANT_VERY_LOW_COST,
    WANT_LOW_COST,
    WANT_AVERAGE_COST,
    WANT_VERY_HIGH_COST,
    WANT_HIGH_COST,
    SHOW_ANY,
    WHAT_EXISTS,
]
