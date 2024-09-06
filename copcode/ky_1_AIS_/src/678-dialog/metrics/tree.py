from typing import List

from ttypes.data import ExtendedLeafData
from ttypes.node import TreeNode


def find_reversed_path(name: str, node: TreeNode, path: List[str]) -> bool:
    if node['children']:
        for child in node['children']:
            if find_reversed_path(name, child, path):
                path.append(node['data']['name'])
                return True
    elif node['data']['name'] == name:
        path.append(name)
        return True
    return False


def get_path(root: TreeNode, name: str) -> List[str]:
    path = []
    find_reversed_path(name, root, path)
    path.reverse()
    return path


def calculate_common_parents(path1: List[str], path2: List[str]) -> int:
    for i in range(len(path1)):
        if path1[i] != path2[i]:
            return i
    return len(path1)


def calculate_tree_distance(root: TreeNode, leaf1: ExtendedLeafData, leaf2: ExtendedLeafData) -> float:
    leaf1.path = get_path(root, leaf1.source['name'])
    leaf2.path = get_path(root, leaf2.source['name'])
    n_common_parents = calculate_common_parents(leaf1.path, leaf2.path)
    return (len(leaf1.path) - n_common_parents) / (len(leaf1.path) - 1)
