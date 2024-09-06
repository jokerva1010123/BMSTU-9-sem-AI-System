from typing import Callable, List

from algorithms.find import find
from ttypes.data import \
    ExtendedLeafData, \
    LEAF_DATA_BOOLEAN_FIELDS, \
    LEAF_DATA_CATEGORICAL_FIELDS, \
    LEAF_DATA_NUMERIC_FIELDS
from ttypes.search import SearchConfig, SearchListConfig, SearchRangeConfig, SearchValueConfig


NUMERIC_AVAILABLE_SEARCH_TYPE_LIST = ['value', 'range']
BOOLEAN_AVAILABLE_SEARCH_TYPE_LIST = ['value']
CATEGORICAL_AVAILABLE_SEARCH_TYPE_LIST = ['list']

SearchRule = Callable[[ExtendedLeafData], bool]


class SearchEngine:
    search_rules: List[SearchRule] = []

    def __init__(self, search_configs: List[SearchConfig]):
        for search_config in search_configs:
            if search_config['name'] in LEAF_DATA_NUMERIC_FIELDS:
                self.__add_numeric_search_rule(search_config)
            elif search_config['name'] in LEAF_DATA_BOOLEAN_FIELDS:
                self.__add_boolean_search_rule(search_config)
            elif find(LEAF_DATA_CATEGORICAL_FIELDS, lambda field: field['name'] == search_config['name']):
                self.__add_categorical_search_rule(search_config)
            else:
                raise Exception(f'Unexpected field name in SearchConfig: {search_config["name"]}')

    def find_all(self, extended_leaves_data: List[ExtendedLeafData]) -> List[ExtendedLeafData]:
        return [extended_leaf_data for extended_leaf_data in extended_leaves_data
                if all(search_rule(extended_leaf_data) for search_rule in self.search_rules)]

    def __add_value_search_rule(self, search_value_config: SearchValueConfig):
        self.search_rules.append(
            lambda extended_leaf_data:
                extended_leaf_data.source[search_value_config['name']] == search_value_config['value']
        )

    def __add_range_search_rule(self, search_range_config: SearchRangeConfig):
        if search_range_config['max'] < search_range_config['min']:
            raise Exception(f'Expected min <= max in SearchRangeConfig for field: {search_range_config["name"]}')

        def f(extended_leaf_data: ExtendedLeafData) -> bool:
            field: str = search_range_config['name']
            value: float = extended_leaf_data.source[field]
            return (search_range_config['min'] <= value) and (value <= search_range_config['max'])

        self.search_rules.append(f)

    def __add_list_search_rule(self, search_list_config: SearchListConfig):
        def f(extended_leaf_data: ExtendedLeafData) -> bool:
            field: str = search_list_config['name']
            value: str = extended_leaf_data.source[field]
            return value in search_list_config['list']

        self.search_rules.append(f)

    def __add_search_rule(self, search_config: SearchConfig, available_search_type_list: List[str], prompt: str):
        if search_config['type'] not in available_search_type_list:
            raise Exception(f'Unexpected search type "{search_config["type"]}"' +
                            f'in SearchConfig for {prompt} field: {search_config["name"]}')

        match search_config['type']:
            case 'value':
                self.__add_value_search_rule(search_config)
            case 'range':
                self.__add_range_search_rule(search_config)
            case 'list':
                self.__add_list_search_rule(search_config)

    def __add_numeric_search_rule(self, search_config: SearchConfig):
        self.__add_search_rule(search_config, NUMERIC_AVAILABLE_SEARCH_TYPE_LIST, 'numeric')

    def __add_boolean_search_rule(self, search_config: SearchConfig):
        self.__add_search_rule(search_config, BOOLEAN_AVAILABLE_SEARCH_TYPE_LIST, 'boolean')

    def __add_categorical_search_rule(self, search_config: SearchConfig):
        self.__add_search_rule(search_config, CATEGORICAL_AVAILABLE_SEARCH_TYPE_LIST, 'categorical')
