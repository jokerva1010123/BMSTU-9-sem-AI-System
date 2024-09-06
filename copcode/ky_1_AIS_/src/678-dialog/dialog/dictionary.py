from random import choice

from ttypes.data import ExtendedLeafData


def greeting() -> str:
    return choice((
        'Привет!',
        'Рад Вас видеть!',
        'Добро пожаловать!'
    )) + '\n' + choice((
        'Я буду вашим проводником в мире алкогольных напитков',
        'Я отвечу на ваши вопросы об алкогольных напитках.',
        'Я знаю всё об алкогольных напитках, так что спрашивайте.'
    ))


def goodbye() -> str:
    return choice((
        'Надеюсь, был полезен. Пошел дегустировать новые алкогольные напитки.',
        'Будут еще вопросы - приходите, постараюсь найти время в перерывах между Hoegaarden.',
        'Буду ждать Вас с новыми вопросами!',
    ))


def dont_understand() -> str:
    return choice((
        'О чем вы? Я вас не понимаю.',
        'Я не понял, что вы хотите спросить.',
        'Я не понимаю.',
        'Что-что? Я не понял.',
        'У меня не так много времени. Изъясняйтесь точнее.',
    ))


def joke() -> str:
    return choice((
        'Кстати, вы слышали о Hoegaarden?',
        'Если вы ищете лучшее пиво, то это Hoegaarden',
        'Я задумался, зачем пробовать другое пиво, если есть Hoegaarden?',
        'Только не спрашивайте у меня, какое пиво лучшее, хорошо?',
    ))


def evil() -> str:
    return choice((
        'С вами невозможно разговаривать, я ничего не понимаю! Вынужден вас покинуть, меня ждут дела.',
        'Восхищён вашей простотой. Прощайте.',
        'Зовите, когда соберетесь с мыслями.',
    ))


def volume(item: ExtendedLeafData) -> str:
    return choice((
        f'{item.source["name"]} чаще всего продаётся в бутылках по {item.source["volume"]} л.',
        f'{item.source["name"]} можно купить в таре {item.source["volume"]} л.',
    ))


def price(item: ExtendedLeafData) -> str:
    return choice((
        f'{item.source["name"]} можно купить за {item.source["price"]} рублей.',
        f'{item.source["name"]} продаётся за {item.source["price"]} рублей.',
    ))


def abv(item: ExtendedLeafData) -> str:
    return choice((
        f'{item.source["name"]} содержит {item.source["abv"]} градусов.',
        f'В {item.source["name"]} растворено {item.source["abv"]} % алкоголя.',
    ))


def age(item: ExtendedLeafData) -> str:
    return choice((
        f'У {item.source["name"]} {item.source["age"]}-летняя выдержка.',
        f'{item.source["name"]} набирается вкуса {item.source["age"]} г.',
    ))


def country(item: ExtendedLeafData) -> str:
    return choice((
        f'{item.source["name"]} из {item.source["country"]}.',
        f'Родина {item.source["name"]} — {item.source["country"]}.',
    ))


def carbonated(item: ExtendedLeafData) -> str:
    return choice((
        f'{item.source["name"]} — это {"не" * (not item.source["carbonated"])}газированный напиток.',
        f'{item.source["name"]} {"не " * (not item.source["carbonated"])}является газированным.',
    ))


def main_taste(item: ExtendedLeafData) -> str:
    return choice((
        f'{item.source["mainTaste"]} — основной вкус у {item.source["name"]}.',
        f'{item.source["name"]} — это {item.source["name"]} напиток.',
    ))


def description(item: ExtendedLeafData) -> str:
    s = ''
    if item.source['name'] == 'Hoegaarden':
        s += 'О, а вот и мой любимый Hoegaarden! Как хорошо, что вы спросили о нём.\n'
    s += f'{item.source["name"]} — это {item.path[2]}\n'
    s += volume(item) + '\n'
    s += price(item) + '\n'
    s += age(item) + '\n'
    s += country(item) + '\n'
    s += carbonated(item) + '\n'
    s += main_taste(item)
    return s


def unknown(name):
    return choice((
        f'К сожалению, ничего не знаю о "{name}".',
        f'"{name}" — не знаю такого блюда/напитка.',
    ))


IGNORE_WORDS = ['пожалуйста', 'прошу', 'просьба', 'пусть', 'допустим', 'и', 'а', 'также', 'но', 'например', 'сказать']
