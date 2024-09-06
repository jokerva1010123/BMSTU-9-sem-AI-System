from typing import List, TypedDict, Union

from ttypes.data import InodeData, LeafData


class TreeNode(TypedDict):
    data: Union[InodeData, LeafData]
    children: List['TreeNode']
