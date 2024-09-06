from typing import List

from algorithms.leaves import get_leaves_data, normalize_leaves_data
from io_util.read_json import read_map
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

    results = [
        [
            {'e': 0.0, 'm': 0.0, 'n': 0.0, 'p': 0.0, 'c': 0.0}
            for _ in range(len(leaves_data))
        ] for _ in range(len(leaves_data))
    ]

    for i, ei in enumerate(extended_leaves_data):
        for j, ej in enumerate(extended_leaves_data):
            results[i][j]['e'] = calculate_euclidean_distance(ei, ej)
            results[i][j]['m'] = calculate_manhattan_distance(ei, ej)
            results[i][j]['n'] = calculate_tree_distance(root, ei, ej)
            results[i][j]['p'] = calculate_pearson_correlation_coefficient(ei, ej)
            results[i][j]['c'] = calculate_custom_distance(root, ei, ej)

    table = '<table>\n\t<tr>\n\t\t<th></th>\n'
    for i in range(len(leaves_data)):
        table += f'\t\t<th>{leaves_data[i]["name"]}</th>\n'
    table += '\t</tr>\n'
    for i in range(len(leaves_data)):
        rows = [f'\t<tr>\n\t\t<th rowspan="5">{leaves_data[i]["name"]}</th>\n',
                '\t<tr>\n', '\t<tr>\n', '\t<tr>\n', '\t<tr>\n']
        letters = ['e', 'm', 'n', 'p', 'c']
        for k in range(len(rows)):
            table += rows[k]
            for j in range(len(leaves_data)):
                table += f'\t\t<td>{results[i][j][letters[k]]}</td>\n'
            table += '\t</tr>\n'
    table += '</table>'
    print(table)


if __name__ == '__main__':
    main()
