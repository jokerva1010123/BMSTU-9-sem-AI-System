import * as alcoholMap from '../../docs/alcohol-map.json';
import {LeafData, ExtendedLeafData} from './types/data';
import {TreeNode} from './types/node';
import {getLeavesData, normalizeLeavesData} from './algorithms/leaves';
import {calculateEuclideanDistance} from './metrics/euclidean';
import {calculateManhattanDistance} from './metrics/manhattan';
import {calculateTreeDistance} from './metrics/tree';
import {calculatePearsonCorrelationCoefficient} from './metrics/pearson';
import {calculateCustomDistance} from './metrics/custom';
import {readProduct} from './io/readProduct';


const lab02 = () => {
	const root: TreeNode = alcoholMap;
	const leavesData: LeafData[] = getLeavesData(root);
	const extendedLeavesData: ExtendedLeafData[] = normalizeLeavesData(leavesData);
	const products: string[] = leavesData.map((leafData: LeafData): string => leafData.name);

	console.log('List of products: ', products);

	const N = 10;
	for (let i = 1; i < N; ++i) {
		console.log(`\nITERATION ${i}`);
		const product1 = readProduct('first', products);
		const product2 = readProduct('second', products);

		const extendedLeafData1 = extendedLeavesData[products.indexOf(product1)];
		const extendedLeafData2 = extendedLeavesData[products.indexOf(product2)];

		const euclideanDistance = calculateEuclideanDistance(extendedLeafData1, extendedLeafData2);
		const manhattanDistance = calculateManhattanDistance(extendedLeafData1, extendedLeafData2);
		const treeDistance = calculateTreeDistance(root, extendedLeafData1, extendedLeafData2);
		const pearsonCorrelationCoefficient = calculatePearsonCorrelationCoefficient(extendedLeafData1, extendedLeafData2);
		const customDistance = calculateCustomDistance(root, extendedLeafData1, extendedLeafData2);

		console.log(`Euclidean distance: ${euclideanDistance}`);
		console.log(`Manhattan distance: ${manhattanDistance}`);
		console.log(`Tree distance: ${treeDistance}`);
		console.log(`Pearson correlation coefficient: ${pearsonCorrelationCoefficient}`);
		console.log(`Custom distance: ${customDistance}`);
	}
};

lab02();
