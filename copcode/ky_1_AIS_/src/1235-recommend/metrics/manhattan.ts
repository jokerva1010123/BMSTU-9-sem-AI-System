import {
	ExtendedLeafData,
	EXTENDED_LEAF_DATA_NORMALIZED_FIELDS,
	EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS,
} from '../types/data';


export const calculateManhattanDistance = (x: ExtendedLeafData, y: ExtendedLeafData): number =>
	EXTENDED_LEAF_DATA_NORMALIZED_FIELDS.reduce(
		(acc: number, cur: string): number =>
			acc + EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS[cur] * Math.abs(y.normalized[cur] - x.normalized[cur]),
		0
	);
