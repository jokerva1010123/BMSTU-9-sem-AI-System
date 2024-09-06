import json

from typing import List

from ttypes.node import TreeNode
from ttypes.search import SearchConfig


def read_json(filepath):
    with open(filepath) as caucasian_cuisine_map:
        return json.load(caucasian_cuisine_map)


def read_map() -> TreeNode:
    return read_json('../../docs/alcohol-map.json')


def read_config() -> List[SearchConfig]:
    return read_json('../../docs/search-config.json')
