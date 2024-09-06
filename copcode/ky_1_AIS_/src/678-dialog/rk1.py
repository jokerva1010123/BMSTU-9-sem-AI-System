from copy import deepcopy
from sys import exit
from typing import List

from algorithms.leaves import get_leaves_data, normalize_leaves_data
from io_util.read_json import read_map, read_config
from io_util.read_product import read_natural_or_zero_number_of, read_products
from recommender.recommend import recommend
from search.approx import ApproxSearchEngine
from search.search import SearchEngine
from ttypes.data import LeafData, ExtendedLeafData
from ttypes.node import TreeNode
from ttypes.search import SearchConfig


class RK1:
    root: TreeNode
    leaves_data: List[LeafData]
    extended_leaves_data: List[ExtendedLeafData]
    working_leaves_data: List[ExtendedLeafData]

    def __init__(self, root: TreeNode):
        self.root = root
        self.leaves_data = get_leaves_data(root)
        self.extended_leaves_data = normalize_leaves_data(self.leaves_data)
        self.working_leaves_data = deepcopy(self.extended_leaves_data)

    def run(self) -> None:
        while True:
            print('0. Reset All')
            print('1. Recommend (LAB 3)')
            print('2. Search (LAB 5)')
            print('3. Quit')
            n = read_natural_or_zero_number_of('menu', 3)
            match n:
                case 0:
                    self.reset()
                case 1:
                    self.recommend()
                case 2:
                    self.search()
                case 3:
                    print('Good bye!')
                    exit()

    def reset(self):
        self.working_leaves_data = deepcopy(self.extended_leaves_data)
        print(end='\033[H\033[J')

    def recommend(self):
        products: List[str] = [leaf_data.source['name'] for leaf_data in self.working_leaves_data]
        print('List of products: ', products)

        likes = read_products('likes', products)
        products_minus_likes = [product for product in products if product not in likes]

        dislikes = read_products('dislikes', products_minus_likes)

        recommendations = recommend(self.root, self.working_leaves_data, likes, dislikes)
        n = read_natural_or_zero_number_of('out recommendations', len(recommendations))
        self.working_leaves_data = recommendations[:n]
        print(self.working_leaves_data)

    def search(self):
        _ = input('Change search-config.json and press any key to search')
        search_configs: List[SearchConfig] = read_config()
        print(search_configs)
        search_engine: SearchEngine = SearchEngine(search_configs)

        search_results = search_engine.find_all(self.working_leaves_data)
        if not search_results:
            approx_search_engine = ApproxSearchEngine(search_configs, self.leaves_data)
            print('========== No exact match found, however you may like :')
            n = read_natural_or_zero_number_of('out recommendations', len(self.working_leaves_data))
            self.working_leaves_data = approx_search_engine.find_all(self.root, self.working_leaves_data)[:n]
            print(self.working_leaves_data)
            return
        print('========== Found:')
        print(search_results)
        self.working_leaves_data = search_results


def main():
    root: TreeNode = read_map()

    rk1 = RK1(root)
    rk1.run()


if __name__ == '__main__':
    main()
