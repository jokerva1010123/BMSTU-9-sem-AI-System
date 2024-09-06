import * as alcoholMap from '../../docs/alcohol-map.json';
import {LeafData, ExtendedLeafData} from './types/data';
import {TreeNode} from './types/node';
import {getLeavesData, normalizeLeavesData} from './algorithms/leaves';
import {calculateEuclideanDistance} from './metrics/euclidean';
import {calculateManhattanDistance} from './metrics/manhattan';
import {calculateTreeDistance} from './metrics/tree';
import {calculatePearsonCorrelationCoefficient} from './metrics/pearson';
import {calculateCustomDistance} from './metrics/custom';


const main = () => {
	const root: TreeNode = alcoholMap;
	const leavesData: LeafData[] = getLeavesData(root);
	const extendedLeavesData: ExtendedLeafData[] = normalizeLeavesData(leavesData);

	const results = Array.from({length: leavesData.length}, () => Array.from({length: leavesData.length}, () => ({e: 0, m: 0, n: 0, p: 0, c: 0})));
	for (let i = 0; i < leavesData.length; ++i) {
		for (let j = 0; j < leavesData.length; ++j) {
			results[i][j] = {
				e: calculateEuclideanDistance(extendedLeavesData[i], extendedLeavesData[j]),
				m: calculateManhattanDistance(extendedLeavesData[i], extendedLeavesData[j]),
				n: calculateTreeDistance(root, extendedLeavesData[i], extendedLeavesData[j]),
				p: calculatePearsonCorrelationCoefficient(extendedLeavesData[i], extendedLeavesData[j]),
				c: calculateCustomDistance(root, extendedLeavesData[i], extendedLeavesData[j]),
			};
		}
	}

	let table = '<table>\n\t<tr>\n\t\t<th></th>\n';
	for (let i = 0; i < leavesData.length; ++i) {
		table += `\t\t<th>${leavesData[i].name}</th>\n`;
	}
	table += '\t</tr>\n';
	for (let i = 0; i < leavesData.length; ++i) {
		const rows = [`\t<tr>\n\t\t<th rowspan="5">${leavesData[i].name}</th>\n`, '\t<tr>\n', '\t<tr>\n', '\t<tr>\n', '\t<tr>\n'];
		const letters = ['e', 'm', 'n', 'p', 'c'];
		for (let k = 0; k < rows.length; ++k) {
			table += rows[k];
			for (let j = 0; j < leavesData.length; ++j) {
				table += `\t\t<td>${results[i][j][letters[k]]}</td>\n`;
			}
			table += '\t</tr>\n';
		}
	}
	table += '</table>';
	console.log(table);
};

main();
