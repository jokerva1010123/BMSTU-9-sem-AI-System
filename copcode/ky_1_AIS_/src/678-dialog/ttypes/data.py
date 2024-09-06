from copy import deepcopy
from typing import List, Optional, TypedDict, Union, Literal


class InodeData(TypedDict):
    name: str


class LeafData(TypedDict):
    name: str
    volume: float
    price: float
    abv: float
    age: float
    country: str
    carbonated: bool
    mainTaste: Union[Literal['bitter'], Literal['sour'], Literal['sweet']]


LEAF_DATA_NUMERIC_FIELDS = ('volume', 'price', 'abv', 'age')
LEAF_DATA_BOOLEAN_FIELDS = ('carbonated',)
LEAF_DATA_CATEGORICAL_FIELDS = (
    {
        'name': 'mainTaste',
        'values': ('bitter', 'sour', 'sweet'),
    },
)


class NormalizedLeafData(TypedDict):
    volume: float
    price: float
    abv: float
    age: float
    carbonated: float
    mainTaste: float


class Score(TypedDict):
    like: float
    dislike: float
    total: float


class ExtendedLeafData:
    source: LeafData
    path: List[str]
    normalized: NormalizedLeafData
    score: Score

    def __init__(self, leaf_data: Optional[LeafData] = None):
        self.source = {
            'name': '__noname__',
            'volume': 0,
            'price': 0,
            'abv': 0,
            'age': 0,
            'country': '__no_country__',
            'carbonated': False,
            'mainTaste': 'bitter',
        }
        self.path = []
        self.normalized = {
            'volume': 0.5,
            'price': 0.5,
            'abv': 0.5,
            'age': 0.5,
            'carbonated': 0.5,
            'mainTaste': 0.5,
        }
        self.score = {
            'like': 0,
            'dislike': 0,
            'total': 0,
        }

        if leaf_data is None:
            return

        self.source = deepcopy(leaf_data)

        for field in LEAF_DATA_NUMERIC_FIELDS:
            self.normalized[field] = leaf_data[field]

        for field in LEAF_DATA_BOOLEAN_FIELDS:
            if field in leaf_data:
                self.normalized[field] = float(leaf_data[field])

        for field in LEAF_DATA_CATEGORICAL_FIELDS:
            self.normalized[field['name']] = \
                field['values'].index(leaf_data[field['name']]) / (len(field['values']) - 1)

    def __repr__(self):
        return f'ELD{{source={self.source}, path={self.path}, normalized={self.normalized}, score={self.score}}}\n'


EXTENDED_LEAF_DATA_NORMALIZED_FIELDS = \
    LEAF_DATA_NUMERIC_FIELDS + \
    LEAF_DATA_BOOLEAN_FIELDS + \
    tuple(field['name'] for field in LEAF_DATA_CATEGORICAL_FIELDS)

EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS = {
    'volume': 1.1,
    'price': 1.5,
    'abv': 1.5,
    'age': 0.8,
    'carbonated': 0.7,
    'mainTaste': 0.4,
}
