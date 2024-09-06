from copy import deepcopy
from typing import List

from algorithms.find import find
from algorithms.leaves import calculate_min_max_of_numeric_fields, fill_paths
from metrics.euclidean import calculate_euclidean_distance
from ttypes.data import \
    LeafData, \
    LEAF_DATA_BOOLEAN_FIELDS, \
    LEAF_DATA_CATEGORICAL_FIELDS, \
    LEAF_DATA_NUMERIC_FIELDS, \
    ExtendedLeafData
from ttypes.node import TreeNode
from ttypes.search import SearchConfig

DEFAULT_MEAN = 0.5


def calculate_mean(sample: List[float]) -> float:
    if not sample:
        return DEFAULT_MEAN
    return sum(sample) / len(sample)


class ApproxSearchEngine:
    search_configs: List[SearchConfig]
    minimums_of_numeric_fields: List[float]
    maximums_of_numeric_fields: List[float]

    def __init__(self, search_configs: List[SearchConfig], leaves_data: List[LeafData]):
        self.search_configs = search_configs
        self.minimums_of_numeric_fields, self.maximums_of_numeric_fields = \
            calculate_min_max_of_numeric_fields(leaves_data)

    def find_all(self, root: TreeNode, extended_leaves_data: List[ExtendedLeafData]) -> List[ExtendedLeafData]:
        average_leaf_data: ExtendedLeafData = ExtendedLeafData()
        self.__fill_numeric_fields(average_leaf_data)
        self.__fill_boolean_fields(average_leaf_data)
        self.__fill_categorical_fields(average_leaf_data)

        working_leaves_data: List[ExtendedLeafData] = deepcopy(extended_leaves_data)
        fill_paths(root, working_leaves_data)
        for workingLeafData in working_leaves_data:
            workingLeafData.score['like'] = calculate_euclidean_distance(workingLeafData, average_leaf_data)
            workingLeafData.score['total'] = workingLeafData.score['like']

        return sorted(working_leaves_data, key=lambda leaf_data: leaf_data.score['total'])

    def __fill_numeric_fields(self, average_leaf_data: ExtendedLeafData):
        for j, field in enumerate(LEAF_DATA_NUMERIC_FIELDS):
            search_config = find(self.search_configs, lambda _search_config: _search_config['name'] == field)
            if search_config is None:
                return

            match search_config['type']:
                case 'value':
                    source_value = search_config['value']
                case 'range':
                    source_value = (search_config['min'] + search_config['max']) / 2
                case _:
                    raise Exception(f'Unexpected search type in find_approx: {search_config["type"]}')

            min_j: float = self.minimums_of_numeric_fields[j]
            max_j: float = self.maximums_of_numeric_fields[j]
            average_leaf_data.normalized[field] = (source_value - min_j) / (max_j - min_j)

    def __fill_boolean_fields(self, average_leaf_data: ExtendedLeafData):
        for field in LEAF_DATA_BOOLEAN_FIELDS:
            search_config = find(self.search_configs, lambda _search_config: _search_config['name'] == field)
            if search_config is None:
                return

            average_leaf_data.normalized[field] = float(search_config['value'])

    def __fill_categorical_fields(self, average_leaf_data: ExtendedLeafData):
        for field in LEAF_DATA_CATEGORICAL_FIELDS:
            search_config = find(self.search_configs, lambda _search_config: _search_config['name'] == field['name'])
            if search_config is None:
                return

            sample = [
                field['values'].index(item) / (len(field['values']) - 1)
                for item in search_config['list']
            ]

            average_leaf_data.normalized[field['name']] = calculate_mean(sample)
