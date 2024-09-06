from metrics.euclidean import calculate_euclidean_distance
from metrics.tree import calculate_tree_distance
from ttypes.data import ExtendedLeafData
from ttypes.node import TreeNode


EW = 0.8
TW = 1.2


def calculate_custom_distance(root: TreeNode, x: ExtendedLeafData, y: ExtendedLeafData) -> float:
    return EW * calculate_euclidean_distance(x, y) + TW * calculate_tree_distance(root, x, y)
