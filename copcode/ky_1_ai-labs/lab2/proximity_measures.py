from pow_distance import calc_distance_in_pow
from tree.genre_node import GenreVisualNode
from tree.tree_tools import calc_distance_between_nodes, get_leafs, calc_max_distance_between_nodes
from tree.node import Node


def calc_euclidean_measure(leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items() if name not in ('name', 'theme')]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items() if name not in ('name', 'theme')]
    #print(leaf_1.name, leaf_2.name, attributes1, attributes2)
    return calc_distance_in_pow(attributes1, attributes2, 2)


def calc_manhattan_measure(leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    attributes1 = [val for name, val in leaf_1.countable_attributes.items() if name in ('name', 'theme')]
    attributes2 = [val for name, val in leaf_2.countable_attributes.items() if name in ('name', 'theme')]
    # attributes1 = [val for name, val in leaf_1.countable_attributes.items()]
    # attributes2 = [val for name, val in leaf_2.countable_attributes.items()]
    return calc_distance_in_pow(attributes1, attributes2, 1)


def calc_tree_distance_measure(
        tree: Node,
        leaf_1: GenreVisualNode,
        leaf_2: GenreVisualNode,
        max_distance_between_nodes: int
):
    return calc_distance_between_nodes(tree, leaf_1.name, leaf_2.name) / max_distance_between_nodes


def generalizing_proximity_measure(tree: Node, leaf_1: GenreVisualNode, leaf_2: GenreVisualNode):
    max_distance_between_artists = calc_max_distance_between_nodes(tree)
    euclidean_proximity = calc_euclidean_measure(leaf_1, leaf_2)
    manhattan_proximity = calc_manhattan_measure(leaf_1, leaf_2)
    tree_distance = calc_tree_distance_measure(tree, leaf_1, leaf_2, max_distance_between_artists)
    generalizing_proximity = euclidean_proximity + manhattan_proximity / 10 + tree_distance
    return generalizing_proximity