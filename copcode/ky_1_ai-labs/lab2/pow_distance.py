from tree.genre_node import VisualNode, GenreVisualNode


def calc_distance_in_pow(attributes1: list[float], attributes2: list[float], power):
    distance = 0
    for i in range(len(attributes1)):
        distance += pow(abs(attributes1[i] - attributes2[i]), power)
    return pow(distance, 1 / power)


# def calc_distance_in_pow(node1: GenreVisualNode, node2: GenreVisualNode, power):
#     distance = 0
#     #print(node1.countable_attributes, node2.countable_attributes)
#     for i in range(len(node1.countable_attributes)):
#         distance += pow(abs(node1.countable_attributes[i] - node2.countable_attributes[i]), power)
#     return pow(distance, 1/power)


