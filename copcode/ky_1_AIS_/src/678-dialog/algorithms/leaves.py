from math import inf
from typing import List, Tuple

from algorithms.flat_map import flat_map
from metrics.tree import get_path
from ttypes.data import LeafData, ExtendedLeafData, LEAF_DATA_NUMERIC_FIELDS
from ttypes.node import TreeNode


def get_leaves_data(node: TreeNode) -> List[LeafData]:
    if node['children']:
        return flat_map(get_leaves_data, node['children'])
    return [node['data']]


def calculate_min_max_of_numeric_fields(leaves_data: List[LeafData]) -> Tuple[List[float], List[float]]:
    minimums_of_numeric_fields = [inf] * len(LEAF_DATA_NUMERIC_FIELDS)
    maximums_of_numeric_fields = [-inf] * len(LEAF_DATA_NUMERIC_FIELDS)
    for leaf_data in leaves_data:
        for j, field in enumerate(LEAF_DATA_NUMERIC_FIELDS):
            minimums_of_numeric_fields[j] = min(leaf_data[field], minimums_of_numeric_fields[j])
            maximums_of_numeric_fields[j] = max(leaf_data[field], maximums_of_numeric_fields[j])
    return minimums_of_numeric_fields, maximums_of_numeric_fields


def normalize_leaves_data(leaves_data: List[LeafData]) -> List[ExtendedLeafData]:
    minimums_of_numeric_fields, maximums_of_numeric_fields = calculate_min_max_of_numeric_fields(leaves_data)
    normalized_leaves_data: List[ExtendedLeafData] = [ExtendedLeafData(leaf_data) for leaf_data in leaves_data]
    for j, field in enumerate(LEAF_DATA_NUMERIC_FIELDS):
        min_j: float = minimums_of_numeric_fields[j]
        max_j: float = maximums_of_numeric_fields[j]
        for i, leaf_data in enumerate(leaves_data):
            normalized_leaves_data[i].normalized[field] = (leaf_data[field] - min_j) / (max_j - min_j)
    return normalized_leaves_data


def fill_paths(root: TreeNode, extended_leaves_data: List[ExtendedLeafData]):
    for extended_leaf_data in extended_leaves_data:
        extended_leaf_data.path = get_path(root, extended_leaf_data.source['name'])
