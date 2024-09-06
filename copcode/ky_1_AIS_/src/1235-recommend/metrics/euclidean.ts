import {
	ExtendedLeafData,
	EXTENDED_LEAF_DATA_NORMALIZED_FIELDS,
	EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS,
} from '../types/data';


export const calculateEuclideanDistance = (x: ExtendedLeafData, y: ExtendedLeafData): number =>
	Math.sqrt(
		EXTENDED_LEAF_DATA_NORMALIZED_FIELDS.reduce(
			(acc: number, cur: string): number =>
				acc + EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS[cur] * (y.normalized[cur] - x.normalized[cur]) ** 2,
			0
		)
	);
