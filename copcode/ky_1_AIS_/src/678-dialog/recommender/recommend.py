from copy import deepcopy
from typing import List

from metrics.custom import calculate_custom_distance
from ttypes.data import ExtendedLeafData
from ttypes.node import TreeNode


def recommend(root: TreeNode, extended_leaves_data: List[ExtendedLeafData], likes: List[str], dislikes: List[str]):
    working_leaves_data: List[ExtendedLeafData] = deepcopy(extended_leaves_data)

    def pred_in(x, xs):
        return x in xs

    def pred_not_in(x, xs):
        return x not in xs

    def filter_working_leaf_data(pred, xs):
        return [leaf_data for leaf_data in working_leaves_data if pred(leaf_data.source['name'], xs)]

    likes_data = filter_working_leaf_data(pred_in, likes)
    working_leaves_data = filter_working_leaf_data(pred_not_in, likes)
    dislikes_data = filter_working_leaf_data(pred_in, dislikes)
    working_leaves_data = filter_working_leaf_data(pred_not_in, dislikes)

    for working_leaf_data in working_leaves_data:
        def score(likes_or_dislikes_data):
            return min([
                calculate_custom_distance(root, working_leaf_data, like_or_dislike_data)
                for like_or_dislike_data in likes_or_dislikes_data
            ])
        working_leaf_data.score['like'] = score(likes_data)
        working_leaf_data.score['dislike'] = score(dislikes_data)

    max_dislike_score = 2
    working_leaves_data.sort(key=lambda leaf: leaf.score['dislike'], reverse=True)

    for i, working_leaf_data in enumerate(working_leaves_data):
        working_leaf_data.score['dislike'] = \
            i * max_dislike_score / (len(working_leaves_data) - 1) if dislikes \
            else 0
        working_leaf_data.score['total'] = working_leaf_data.score['like'] + working_leaf_data.score['dislike']

    return sorted(working_leaves_data, key=lambda leaf: leaf.score['total'])
