import {getPath} from "../metrics/tree";
import {ExtendedLeafData, LEAF_DATA_NUMERIC_FIELDS, LeafData} from '../types/data';
import {TreeNode} from '../types/node';


export const getLeavesData = (node: TreeNode): LeafData[] =>
	node.children.length
		? node.children.flatMap(getLeavesData)
		: [node.data as LeafData];

type MinMaxRet = {
	minimumsOfNumericFields: number[],
	maximumsOfNumericFields: number[],
};

export const calculateMinMaxOfNumericFields = (leavesData: LeafData[]): MinMaxRet => {
	const minimumsOfNumericFields = Array(LEAF_DATA_NUMERIC_FIELDS.length).fill(Infinity);
	const maximumsOfNumericFields = Array(LEAF_DATA_NUMERIC_FIELDS.length).fill(-Infinity);
	for (let i = 0; i < leavesData.length; ++i) {
		for (let j = 0; j < LEAF_DATA_NUMERIC_FIELDS.length; ++j) {
			const field: string = LEAF_DATA_NUMERIC_FIELDS[j];
			minimumsOfNumericFields[j] = Math.min(leavesData[i][field], minimumsOfNumericFields[j]);
			maximumsOfNumericFields[j] = Math.max(leavesData[i][field], maximumsOfNumericFields[j]);
		}
	}
	return {minimumsOfNumericFields, maximumsOfNumericFields};
};

export const normalizeLeavesData = (leavesData: LeafData[]): ExtendedLeafData[] => {
	const {minimumsOfNumericFields, maximumsOfNumericFields} = calculateMinMaxOfNumericFields(leavesData);
	const normalizedLeavesData: ExtendedLeafData[] = leavesData.map((leafData: LeafData): ExtendedLeafData => new ExtendedLeafData(leafData));
	for (let i = 0; i < leavesData.length; ++i) {
		for (let j = 0; j < LEAF_DATA_NUMERIC_FIELDS.length; ++j) {
			const field: string = LEAF_DATA_NUMERIC_FIELDS[j];
			const min: number = minimumsOfNumericFields[j];
			const max: number = maximumsOfNumericFields[j];
			normalizedLeavesData[i].normalized[field] = (leavesData[i][field] - min) / (max - min);
		}
	}
	return normalizedLeavesData;
};

export const fillPaths = (root: TreeNode, extendedLeavesData: ExtendedLeafData[]) => {
	extendedLeavesData.forEach(
		(extendedLeafData: ExtendedLeafData) => {
			extendedLeafData.path = getPath(root, extendedLeafData.source.name);
		}
	);
};
