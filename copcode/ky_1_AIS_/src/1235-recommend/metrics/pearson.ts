import {
	ExtendedLeafData,
	EXTENDED_LEAF_DATA_NORMALIZED_FIELDS,
	EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS,
} from '../types/data';


const EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS_SUM =
	EXTENDED_LEAF_DATA_NORMALIZED_FIELDS.reduce(
		(acc: number, cur: string): number =>
			acc + EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS[cur],
		0
	);

const calculateMean = (x: ExtendedLeafData): number =>
	EXTENDED_LEAF_DATA_NORMALIZED_FIELDS.reduce(
		(acc: number, cur: string): number =>
			acc + EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS[cur] * x.normalized[cur],
		0
	) / EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS_SUM;

export const calculatePearsonCorrelationCoefficient = (x: ExtendedLeafData, y: ExtendedLeafData): number => {
	const meanX = calculateMean(x);
	const meanY = calculateMean(y);

	let covariance = 0;
	let varianceX = 0;
	let varianceY = 0;
	EXTENDED_LEAF_DATA_NORMALIZED_FIELDS.forEach((field: string) => {
		const weight = EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS[field];
		covariance += weight * (x.normalized[field] - meanX) * (y.normalized[field] - meanY);
		varianceX += weight * (x.normalized[field] - meanX) ** 2;
		varianceY += weight * (y.normalized[field] - meanY) ** 2;
	});

	return covariance / Math.sqrt(varianceX * varianceY);
};
