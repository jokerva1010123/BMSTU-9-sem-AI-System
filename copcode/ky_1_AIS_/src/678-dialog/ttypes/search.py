from typing import List, Literal, TypedDict, Union


class SearchValueConfig(TypedDict):
    name: str
    type: Literal['value']
    value: float


class SearchRangeConfig(TypedDict):
    name: str
    type: Literal['range']
    min: float
    max: float


class SearchListConfig(TypedDict):
    name: str
    type: Literal['list']
    list: List[str]


SearchConfig = Union[SearchValueConfig, SearchRangeConfig, SearchListConfig]
