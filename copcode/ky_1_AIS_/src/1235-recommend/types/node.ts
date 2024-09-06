import {InodeData, LeafData} from './data';


export type TreeNode = {
	data: InodeData | LeafData,
	children: TreeNode[],
};
