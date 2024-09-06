import {simpleDeepCopy} from '../algorithms/copy';
import {calculateMinMaxOfNumericFields, fillPaths} from '../algorithms/leaves';
import {calculateEuclideanDistance} from '../metrics/euclidean';
import {
	LeafData,
	LEAF_DATA_BOOLEAN_FIELDS,
	LEAF_DATA_CATEGORICAL_FIELDS,
	LEAF_DATA_NUMERIC_FIELDS,
	ExtendedLeafData,
} from '../types/data';
import {TreeNode} from '../types/node';
import {SearchConfig, SearchListConfig, SearchRangeConfig, SearchValueConfig} from '../types/search';

const DEFAULT_MEAN = 0.5;
const calculateMean = (sample: number[]): number =>
	sample.length
		? sample.reduce(
		(acc: number, cur: number): number =>
			acc + cur,
		0
	) / sample.length
		: DEFAULT_MEAN;

export class ApproxSearchEngine {
	searchConfigs: SearchConfig[] = [];
	minimumsOfNumericFields: number[];
	maximumsOfNumericFields: number[];

	constructor(searchConfigs: SearchConfig[], leavesData: LeafData[]) {
		this.searchConfigs = searchConfigs;
		const {minimumsOfNumericFields, maximumsOfNumericFields} = calculateMinMaxOfNumericFields(leavesData);
		this.minimumsOfNumericFields = minimumsOfNumericFields;
		this.maximumsOfNumericFields = maximumsOfNumericFields;
	}

	public findAll(root: TreeNode, extendedLeavesData: ExtendedLeafData[]): ExtendedLeafData[] {
		const averageLeafData: ExtendedLeafData = new ExtendedLeafData();
		this.fillNumericFields(averageLeafData);
		this.fillBooleanFields(averageLeafData);
		this.fillCategoricalFields(averageLeafData);

		const workingLeavesData: ExtendedLeafData[] = simpleDeepCopy(extendedLeavesData);
		fillPaths(root, workingLeavesData);
		workingLeavesData.forEach((workingLeafData: ExtendedLeafData) => {
			workingLeafData.score.like = calculateEuclideanDistance(workingLeafData, averageLeafData);
			workingLeafData.score.total = workingLeafData.score.like;
		});

		return workingLeavesData.sort((lhs: ExtendedLeafData, rhs: ExtendedLeafData): number => lhs.score.total - rhs.score.total);
	}

	private fillNumericFields(averageLeafData: ExtendedLeafData) {
		LEAF_DATA_NUMERIC_FIELDS.forEach(
			(field: string, j: number) => {
				const searchConfig = this.searchConfigs.find(_searchConfig => _searchConfig.name === field);
				if (typeof searchConfig === 'undefined') {
					return;
				}
				let sourceValue = 0;
				switch (searchConfig.type) {
					case 'value': {
						const searchValueConfig = searchConfig as SearchValueConfig;
						sourceValue = searchValueConfig.value;
						break;
					}
					case 'range': {
						const searchRangeConfig = searchConfig as SearchRangeConfig;
						sourceValue = (searchRangeConfig.min + searchRangeConfig.max) / 2;
						break;
					}
					default:
						throw new Error(`Unexpected search type in findApprox: ${searchConfig.type}`);
				}
				const min: number = this.minimumsOfNumericFields[j];
				const max: number = this.maximumsOfNumericFields[j];
				averageLeafData.normalized[field] = (sourceValue - min) / (max - min);
			}
		);
	}

	private fillBooleanFields = (averageLeafData: ExtendedLeafData) => {
		LEAF_DATA_BOOLEAN_FIELDS.forEach(
			(field: string) => {
				const searchConfig = this.searchConfigs.find(_searchConfig => _searchConfig.name === field);
				if (typeof searchConfig === 'undefined') {
					return;
				}
				averageLeafData.normalized[field] = Number((searchConfig as SearchValueConfig).value);
			}
		);
	};

	private fillCategoricalFields = (averageLeafData: ExtendedLeafData) => {
		LEAF_DATA_CATEGORICAL_FIELDS.forEach(
			({name, values}) => {
				const searchConfig = this.searchConfigs.find(_searchConfig => _searchConfig.name === name);
				if (typeof searchConfig === 'undefined') {
					return;
				}
				const searchListConfig = searchConfig as SearchListConfig;
				const sample = searchListConfig.list.map(
					(item: string): number =>
						values.indexOf(item) / (values.length - 1)
				);
				averageLeafData.normalized[name] = calculateMean(sample);
			}
		);
	}
}
