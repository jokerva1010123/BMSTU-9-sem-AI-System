from typing import List

from algorithms.leaves import get_leaves_data, normalize_leaves_data
from io_util.read_json import read_map, read_config
from search.approx import ApproxSearchEngine
from search.search import SearchEngine
from ttypes.data import LeafData, ExtendedLeafData
from ttypes.node import TreeNode
from ttypes.search import SearchConfig


# 0.33 - 1
# 130 - 9800
# 4 - 40
# 1 - 12
# 'bitter' | 'sour' | 'sweet'

def main() -> None:
    root: TreeNode = read_map()
    leaves_data: List[LeafData] = get_leaves_data(root)
    extended_leaves_data: List[ExtendedLeafData] = normalize_leaves_data(leaves_data)

    search_configs: List[SearchConfig] = read_config()
    print(search_configs)
    search_engine = SearchEngine(search_configs)

    search_results = search_engine.find_all(extended_leaves_data)
    if not search_results:
        limit = 5
        approx_search_engine = ApproxSearchEngine(search_configs, leaves_data)
        print('=== Не найдено точного соответствия, однако, возможно, Вам понравится:')
        print(approx_search_engine.find_all(root, extended_leaves_data)[:limit])
        return
    print('===  Найдено:')
    print(search_results)


if __name__ == '__main__':
    main()
