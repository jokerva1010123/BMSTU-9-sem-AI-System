from tree.visual_node import VisualNode, Node
from tree.tree_tools import calc_distance_between_nodes, get_leafs, find_path_to_node, calc_max_distance_between_nodes
from tree.tree_loader import load_tree_dict, create_tree_from_json, get_artists
from tree.genre_node import GenreVisualNode
from proximity_measures import calc_euclidean_measure, calc_manhattan_measure, generalizing_proximity_measure, calc_tree_distance_measure
from plot import plot
from numpy import std


def get_pirson_coeff(x: list, y: list, n):
    x_avg = sum(x) / len(x)
    y_avg = sum(y) / len(y)
    sigma = 0
    for i in range(len(x)):
        sigma += (x[i] - x_avg) * (y[i] - y_avg)
    r_xy = sigma / ((n - 1) * std(x) * std(y))
    return r_xy


def format_print(values: list, column_width: list[int], number_symbols_after_comma=5):
    assert column_width
    current_column_width = 0
    for i, value in enumerate(values):
        if len(column_width) - 1 >= i:
            current_column_width = column_width[i]
        if isinstance(value, float):
            value = round(value, number_symbols_after_comma)
        print(str(value).ljust(current_column_width), end=' ')
    print()


def compare_measures(tree, artist_pairs):
    euclidean_proximity = []
    manhattan_proximity = []
    tree_distance_proximity = []
    generalizing_proximity = []
    max_distance_between_artists = calc_max_distance_between_nodes(tree)
    for artist1, artist2 in artist_pairs:
        euclidean_proximity.append(calc_euclidean_measure(artist1, artist2))
        manhattan_proximity.append(calc_manhattan_measure(artist1, artist2))
        tree_distance_proximity.append(calc_tree_distance_measure(tree, artist1, artist2, max_distance_between_artists))
        generalizing_proximity.append(generalizing_proximity_measure(tree, artist1, artist2))

    artist_names = [(artist1.name + ' - ' + artist2.name) for artist1, artist2 in artist_pairs]
    format_print(['artists', 'generalizing', 'euclidean', 'manhattan', 'tree distance'], [25, 15])
    for i in range(len(artist_names)):
        format_print(
            [artist_names[i], generalizing_proximity[i], euclidean_proximity[i], manhattan_proximity[i],
             tree_distance_proximity[i]],
            column_width=[25, 15],
            number_symbols_after_comma=5
        )


if __name__ == '__main__':
    tree = create_tree_from_json('genres.json')

    # tree.render_tree()
    # VisualNode.show_tree(tree)

    ## ноды для мер близости
    atl = Node.get_child_by_name(tree, 'atl')
    marlow = Node.get_child_by_name(tree, 'slava marlow')
    max_korj = Node.get_child_by_name(tree, 'макс корж')
    lsp = Node.get_child_by_name(tree, 'лсп')
    mukka = Node.get_child_by_name(tree, 'мукка')
    krovostok = Node.get_child_by_name(tree, 'кровосток')
    liga = Node.get_child_by_name(tree, 'лигалайз')
    jah = Node.get_child_by_name(tree, 'jah khalib')
    artists = [atl, marlow, max_korj, lsp, mukka, krovostok]

    ## сравнение
    artist_pairs = [(marlow, max_korj), (lsp, marlow), (lsp, max_korj), (lsp, atl), (lsp, mukka), (lsp, krovostok), (krovostok, mukka), (liga, jah)]
    compare_measures(tree, artist_pairs)

    ##
    # leafs = []
    # get_leafs(tree, leafs)
    # x = [leaf.countable_attributes['year_of_birth'] for leaf in leafs]
    # y = [leaf.countable_attributes['theme'] for leaf in leafs]
    # print(get_pirson_coeff(x, y, len(leafs)))





