import {ExtendedLeafData} from '../types/data';
import {TreeNode} from '../types/node';
import {calculateEuclideanDistance} from './euclidean';
import {calculateTreeDistance} from './tree';


const EW = 0.8;
const TW = 1.2;

export const calculateCustomDistance = (root: TreeNode, x: ExtendedLeafData, y: ExtendedLeafData): number =>
	EW * calculateEuclideanDistance(x, y) + TW * calculateTreeDistance(root, x, y);
