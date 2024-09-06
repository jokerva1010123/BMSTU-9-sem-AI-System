from random import choice, random
import re
from enum import Enum
from typing import List, Optional

from pymorphy2 import MorphAnalyzer

from .dictionary import *

from algorithms.leaves import get_leaves_data, normalize_leaves_data, fill_paths
from io_util.read_json import read_map
from recommender.recommend import recommend
from ttypes.data import LeafData, ExtendedLeafData
from ttypes.node import TreeNode

description_p = r'(\s?(описание|описать|(рассказать о))\s?)'
thanks_p = r'(\s?(спасибо|благодарить)\s?)'
bye_p = r'(\s?(пока|(до свидание))\s?)'
recommendation_p = r'(подобрать|посоветовать|подсказать|порекомендовать|какой выбрать)'


class State(Enum):
    INITIAL = 0
    VOLUME = 1
    PRICE = 2
    ABV = 3
    AGE = 4
    COUNTRY = 5
    CARBONATED = 6
    MAIN_TASTE = 7
    DESCRIPTION = 8
    RECOMMENDATION = 9
    HELP = 10
    EVIL = 11
    COMPLETION = 12


class Dialog:
    def __init__(self, max_angry_level: int = 3, joker_level: float = 0.1):
        self.__state: State = State.INITIAL
        self.__sentence: str = ''

        self.__morph: MorphAnalyzer = MorphAnalyzer()

        self.__angry_level: int = 0
        self.__MAX_ANGRY_LEVEL: int = max_angry_level
        self.__JOKER_COEFFICIENT: float = joker_level

        self.__root: TreeNode = read_map()
        self.__leaves_data: List[LeafData] = get_leaves_data(self.__root)
        self.__extended_leaves_data: List[ExtendedLeafData] = normalize_leaves_data(self.__leaves_data)
        fill_paths(self.__root, self.__extended_leaves_data)

    def __get_item(self, name: str) -> Optional[ExtendedLeafData]:
        for extended_leaf_data in self.__extended_leaves_data:
            if extended_leaf_data.source['name'].lower() == name:
                return extended_leaf_data
        return None

    def run(self) -> None:
        self.__print(greeting())

        while True:
            match self.__state:
                case State.INITIAL:
                    self.__initial_state()
                case State.VOLUME:
                    self.__volume_state()
                    self.__joke()
                case State.PRICE:
                    self.__price_state()
                    self.__joke()
                case State.ABV:
                    self.__abv_state()
                    self.__joke()
                case State.AGE:
                    self.__age_state()
                    self.__joke()
                case State.COUNTRY:
                    self.__country_state()
                    self.__joke()
                case State.CARBONATED:
                    self.__carbonated_state()
                    self.__joke()
                case State.MAIN_TASTE:
                    self.__main_taste_state()
                    self.__joke()
                case State.DESCRIPTION:
                    self.__description_state()
                    self.__joke()
                case State.RECOMMENDATION:
                    self.__recommendation_state()
                    self.__joke()
                case State.HELP:
                    self.__help_state()
                case State.EVIL:
                    self.__print(evil())
                    return
                case State.COMPLETION:
                    self.__print(goodbye())
                    return

    def __initial_state(self) -> None:
        self.__input()

        if \
                re.search(r'сколько (милли)?литр', self.__sentence) or \
                re.match(r'(какой )?объём', self.__sentence):
            self.__state = State.VOLUME

        elif \
                re.match(r'сколько стоить', self.__sentence) or \
                re.match(r'почём', self.__sentence) or \
                re.match(r'(по )?какой (цена|стоимость)', self.__sentence):
            self.__state = State.PRICE

        elif \
                re.match(r'(какой|сколько) процент', self.__sentence):
            self.__state = State.ABV

        elif \
                re.match('какой возраст', self.__sentence) or \
                re.match('как стар', self.__sentence):
            self.__state = State.AGE

        elif \
                re.match('из какой страна', self.__sentence) or \
                re.match('откуда', self.__sentence):
            self.__state = State.COUNTRY

        elif \
                re.match('газированный ли', self.__sentence):
            self.__state = State.CARBONATED

        elif \
                re.match('какой (основной )?вкус', self.__sentence):
            self.__state = State.MAIN_TASTE

        elif re.match(r'где (можно )?купить', self.__sentence):
            self.__state = State.WHERE

        elif re.match(rf'{description_p}', self.__sentence):
            self.__state = State.DESCRIPTION

        elif re.match(rf'{thanks_p}?{bye_p}', self.__sentence):
            self.__state = State.COMPLETION

        elif re.match(rf'{recommendation_p}', self.__sentence):
            self.__state = State.RECOMMENDATION

        elif re.match(rf'что( ты| вы)? (уметь|можешь)', self.__sentence):
            self.__state = State.HELP

        if self.__state != State.INITIAL:
            self.__angry_level = 0
        else:
            self.__angry_level += 1
            if self.__angry_level == self.__MAX_ANGRY_LEVEL:
                self.__state = State.EVIL
            else:
                self.__print(dont_understand())

    def __template_state(self, callback):
        name = self.__sentence.split()[-1]
        item = self.__get_item(name)
        if item is not None:
            self.__print(callback(item))
        else:
            self.__print(unknown(name))
        self.__state = State.INITIAL

    def __volume_state(self) -> None:
        self.__template_state(volume)

    def __price_state(self) -> None:
        self.__template_state(price)

    def __abv_state(self) -> None:
        self.__template_state(abv)

    def __age_state(self) -> None:
        self.__template_state(age)

    def __country_state(self) -> None:
        self.__template_state(country)

    def __carbonated_state(self) -> None:
        self.__template_state(carbonated)

    def __main_taste_state(self) -> None:
        self.__template_state(main_taste)

    def __description_state(self) -> None:
        self.__template_state(description)

    def __recommendation_state(self) -> None:
        s = re.sub(rf'{recommendation_p}', '', self.__sentence)

        none = 999999
        p_min = -none
        p_max = none
        if m := re.search(r'от (\d+)', s):
            p_min = max(int(m.group(1)), p_min)
            s = re.sub(r'от (\d+)', '', s)
        if m := re.search(r'до (\d+)', s):
            p_max = min(int(m.group(1)), p_max)
            s = re.sub(r'до (\d+)', '', s)
        if m := re.search(r'не маленький (\d+)', s):
            p_min = max(int(m.group(1)), p_min)
            s = re.sub(r'не маленький (\d+)', '', s)
        if m := re.search(r'не большой (\d+)', s):
            p_max = min(int(m.group(1)), p_max)
            s = re.sub(r'не большой (\d+)', '', s)
        if m := re.search(r'маленький (\d+)', s):
            p_max = min(int(m.group(1)) - 1, p_max)
            s = re.sub(r'маленький (\d+)', '', s)
        if m := re.search(r'большой (\d+)', s):
            p_min = max(int(m.group(1)) + 1, p_min)
            s = re.sub(r'большой (\d+)', '', s)
        if p_min != -none:
            print(f'min = {p_min}')
        if p_max != none:
            print(f'max = {p_max}')

        typing = []
        discard = []
        if ' не ром' in s:
            discard.append('Rum')
        elif 'ром' in s:
            typing.append('Rum')
        if ' не водка' in s:
            discard.append('Vodka')
        elif 'водка' in s:
            typing.append('Vodka')
        if ' не виски' in s:
            discard.append('Whiskey')
        elif 'виски' in s:
            typing.append('Whiskey')
        if ' не пиво' in s:
            discard.append('Beer')
        elif 'пиво' in s:
            typing.append('Beer')
        if ' не вино' in s:
            discard.append('Wine')
        elif 'вино' in s:
            typing.append('Wine')
        if ' не вермут' in s:
            discard.append('Vermouth')
        elif 'вермут' in s:
            typing.append('Vermouth')
        if not typing:
            typing = ['Rum', 'Vodka', 'Whiskey', 'Beer', 'Wine', 'Vermouth']

        is_carbonated = [True, False]
        if 'негаз' in s:
            is_carbonated = [False]
        elif 'газ' in s:
            is_carbonated = [True]

        self.__print('Какие напитки вам больше всего нравятся?')
        likes = []
        for name in self.__input().split():
            item = self.__get_item(name)
            if item is None:
                self.__print(unknown(name))
            else:
                likes.append(item.source['name'])

        self.__print('А какие вы не любите?')
        dislikes = []
        for name in self.__input().split():
            item = self.__get_item(name)
            if item is None:
                self.__print(unknown(name))
            else:
                dislikes.append(item.source['name'])

        if 'hoegaarden' in dislikes:
            self.__print('Не любите Hoegaarden?! Сделаю вид, что не видел этого..')
            self.__angry_level = self.__MAX_ANGRY_LEVEL - 1

        recommendation = recommend(self.__root, self.__extended_leaves_data, likes, dislikes)

        out = []
        for extended_leaf_data in recommendation:
            if \
                    extended_leaf_data.path[2] in typing and \
                    extended_leaf_data.path[2] not in discard and \
                    extended_leaf_data.source['carbonated'] in is_carbonated:
                if \
                        p_min != -none and \
                        extended_leaf_data.source['price'] < p_min:
                    continue
                if \
                        p_max != none and \
                        extended_leaf_data.source['price'] > p_max:
                    continue
                out.append(extended_leaf_data)

        if out:
            self.__print('Советую:')
            for i, item in enumerate(out):
                self.__print(i + 1)
                self.__print(description(item))
        else:
            self.__print('К сожалению, точного соответствия не нашёл, однако, возможно, вам понравится:')
            recommendation_without_discard = [item for item in recommendation if item.path[2] not in discard]
            for i, item in enumerate(recommendation_without_discard[:3]):
                self.__print(i + 1)
                self.__print(description(item))

        self.__state = State.INITIAL

    def __help_state(self) -> None:
        self.__print('Я могу рассказать об алкогольных напитках, что-нибудь порекомендовать, '
                     'или же разозлиться и уйти, если будете понапрасну тратить мое время.')

        self.__state = State.INITIAL

    def __joke(self) -> None:
        if random() < self.__JOKER_COEFFICIENT:
            self.__print(joke())

    def __input(self):
        sentence = input().translate(str.maketrans('', '', r"!$%&()*,-./:;<=>?@[\]^_`{|}~"))
        words = sentence.split()
        normal_words = [self.__morph.parse(word)[0].normal_form for word in words if word not in IGNORE_WORDS]
        self.__sentence = ' '.join(normal_words)
        print(self.__sentence)
        return self.__sentence

    @staticmethod
    def __print(*args) -> None:
        print('\033[94m', *args, '\033[0m', sep='')
