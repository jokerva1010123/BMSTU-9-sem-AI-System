import {ExtendedLeafData} from '../types/data';
import {TreeNode} from '../types/node';


const findReversedPath = (name: string, node: TreeNode, path: string[]): boolean => {
	if (node.children.length) {
		for (const child of node.children) {
			if (findReversedPath(name, child, path)) {
				path.push(node.data.name);
				return true;
			}
		}
	} else if (node.data.name === name) {
		path.push(name);
		return true;
	}
	return false;
};

export const getPath = (root: TreeNode, name: string): string[] => {
	const path = [];
	findReversedPath(name, root, path);
	path.reverse();
	return path;
};

const calculateCommonParents = (path1: string[], path2: string[]): number => {
	for (let i = 0; i < path1.length; ++i) {
		if (path1[i] !== path2[i]) {
			return i;
		}
	}
	return path1.length;
};

export const calculateTreeDistance = (root: TreeNode, leaf1: ExtendedLeafData, leaf2: ExtendedLeafData): number => {
	leaf1.path = getPath(root, leaf1.source.name);
	leaf2.path = getPath(root, leaf2.source.name);
	const nCommonParents = calculateCommonParents(leaf1.path, leaf2.path);
	return (leaf1.path.length - nCommonParents) / (leaf1.path.length - 1);
};
