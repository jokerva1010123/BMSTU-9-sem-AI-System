from .node import Node
from .genre_node import GenreVisualNode


def find_path_to_node(root: Node, path: list, node_name: str):
    if root is None:
        return

    path.append(root.value)

    if root.value == node_name:
        return path

    for child in root.children:
        if find_path_to_node(child, path, node_name):
            return path

    path.pop()
    return


def calc_distance_between_nodes(root, node_name1: str, node_name2: str):
    if root:
        path1 = find_path_to_node(root, [], node_name1)
        path2 = find_path_to_node(root, [], node_name2)

        i = 0
        while i < len(path1) and i < len(path2):
            if path1[i] != path2[i]:
                break
            i = i + 1

        return len(path1) + len(path2) - 2 * i
    else:
        return 0


def calc_max_distance_between_nodes(tree: Node):
    leafs = []
    get_leafs(tree, leafs)
    leafs = [leaf for leaf in leafs if isinstance(leaf, GenreVisualNode)]

    # найти путь от каждого до каждого и выбрать самый большой
    max_distance_between_artists = 0
    for leaf1 in leafs:
        for leaf2 in leafs:
            if leaf1 != leaf2:
                distance_between_artists = calc_distance_between_nodes(tree, leaf1.name, leaf2.name)
                if distance_between_artists > max_distance_between_artists:
                    max_distance_between_artists = distance_between_artists
    return max_distance_between_artists


def get_leafs(root: Node, leafs: list):
    if not root.children:
        return root
    for child in root.children:
        res = get_leafs(child, leafs)
        if res and isinstance(res, GenreVisualNode):
            leafs.append(res)