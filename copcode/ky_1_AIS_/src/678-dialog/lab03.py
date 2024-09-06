from typing import List

from algorithms.leaves import get_leaves_data, normalize_leaves_data
from io_util.read_json import read_map
from io_util.read_product import read_products
from recommender.recommend import recommend
from ttypes.data import LeafData, ExtendedLeafData
from ttypes.node import TreeNode


def main() -> None:
    root: TreeNode = read_map()
    leaves_data: List[LeafData] = get_leaves_data(root)
    extended_leaves_data: List[ExtendedLeafData] = normalize_leaves_data(leaves_data)
    products: List[str] = [leaf_data['name'] for leaf_data in leaves_data]

    print('List of products: ', products)

    likes = read_products('likes', products)
    products_minus_likes = [product for product in products if product not in likes]

    dislikes = read_products('dislikes', products_minus_likes)

    recommendations = recommend(root, extended_leaves_data, likes, dislikes)
    print(recommendations)


if __name__ == '__main__':
    main()
