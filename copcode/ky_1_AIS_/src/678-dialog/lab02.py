from typing import List

from algorithms.leaves import get_leaves_data, normalize_leaves_data
from io_util.read_json import read_map
from io_util.read_product import read_product
from metrics.custom import calculate_custom_distance
from metrics.euclidean import calculate_euclidean_distance
from metrics.manhattan import calculate_manhattan_distance
from metrics.tree import calculate_tree_distance
from metrics.pearson import calculate_pearson_correlation_coefficient
from ttypes.data import LeafData, ExtendedLeafData
from ttypes.node import TreeNode


def main() -> None:
    root: TreeNode = read_map()
    leaves_data: List[LeafData] = get_leaves_data(root)
    extended_leaves_data: List[ExtendedLeafData] = normalize_leaves_data(leaves_data)
    products: List[str] = [leaf_data['name'] for leaf_data in leaves_data]

    print('List of products: ', products)

    n = 10
    for i in range(n):
        print(f'\nITERATION {i}')
        product1 = read_product('first', products)
        product2 = read_product('second', products)

        e1 = extended_leaves_data[products.index(product1)]
        e2 = extended_leaves_data[products.index(product2)]

        euclidean_distance = calculate_euclidean_distance(e1, e2)
        manhattan_distance = calculate_manhattan_distance(e1, e2)
        tree_distance = calculate_tree_distance(root, e1, e2)
        pearson_correlation_coefficient = calculate_pearson_correlation_coefficient(e1, e2)
        custom_distance = calculate_custom_distance(root, e1, e2)

        print(f'Euclidean distance: {euclidean_distance}')
        print(f'Manhattan distance: {manhattan_distance}')
        print(f'Tree distance: {tree_distance}')
        print(f'Pearson correlation coefficient: {pearson_correlation_coefficient}')
        print(f'Custom distance: {custom_distance}')


if __name__ == '__main__':
    main()
