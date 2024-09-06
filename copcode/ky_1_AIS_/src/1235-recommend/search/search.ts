import {
	ExtendedLeafData,
	LEAF_DATA_BOOLEAN_FIELDS,
	LEAF_DATA_CATEGORICAL_FIELDS,
	LEAF_DATA_NUMERIC_FIELDS,
} from '../types/data';

import {SearchConfig, SearchListConfig, SearchRangeConfig, SearchValueConfig} from '../types/search';

const NUMERIC_AVAILABLE_SEARCH_TYPE_LIST = ['value', 'range'];
const BOOLEAN_AVAILABLE_SEARCH_TYPE_LIST = ['value'];
const CATEGORICAL_AVAILABLE_SEARCH_TYPE_LIST = ['list'];

type SearchRule = (extendedLeafData: ExtendedLeafData) => boolean;

export class SearchEngine {
	searchRules: SearchRule[] = [];

	constructor(searchConfigs: SearchConfig[]) {
		searchConfigs.forEach((searchConfig: SearchConfig) => {
			if (LEAF_DATA_NUMERIC_FIELDS.includes(searchConfig.name)) {
				this.addNumericSearchRule(searchConfig);
			} else if (LEAF_DATA_BOOLEAN_FIELDS.includes(searchConfig.name)) {
				this.addBooleanSearchRule(searchConfig);
			} else if (LEAF_DATA_CATEGORICAL_FIELDS.findIndex(field => field.name === searchConfig.name) !== -1) {
				this.addCategoricalSearchRule(searchConfig);
			} else {
				throw new Error(`Unexpected field name in SearchConfig: ${searchConfig.name}`);
			}
		});
	}

	public findAll(extendedLeavesData: ExtendedLeafData[]): ExtendedLeafData[] {
		return extendedLeavesData.filter(
			(extendedLeafData: ExtendedLeafData): boolean =>
				this.searchRules.every(
					(searchRule: SearchRule): boolean =>
						searchRule(extendedLeafData)
				)
		);
	}

	private addValueSearchRule(searchValueConfig: SearchValueConfig) {
		this.searchRules.push(
			(extendedLeafData: ExtendedLeafData): boolean =>
				extendedLeafData.source[searchValueConfig.name] === searchValueConfig.value
		);
	}

	private addRangeSearchRule(searchRangeConfig: SearchRangeConfig) {
		if (searchRangeConfig.max < searchRangeConfig.min) {
			throw new Error(`Expected min <= max in SearchRangeConfig for field: ${searchRangeConfig.name}`);
		}
		this.searchRules.push(
			(extendedLeafData: ExtendedLeafData): boolean => {
				const field: string = searchRangeConfig.name;
				const value: number = extendedLeafData.source[field];
				return searchRangeConfig.min <= value && value <= searchRangeConfig.max;
			}
		);
	}

	private addListSearchRule(searchListConfig: SearchListConfig) {
		this.searchRules.push(
			(extendedLeafData: ExtendedLeafData): boolean => {
				const field: string = searchListConfig.name;
				const value: string = extendedLeafData.source[field];
				return searchListConfig.list.includes(value);
			}
		);
	}

	private addSearchRule(searchConfig: SearchConfig, availableSearchTypeList: string[], prompt: string) {
		if (!availableSearchTypeList.includes(searchConfig.type)) {
			throw new Error(`Unexpected search type '${searchConfig.type}' in SearchConfig for ${prompt} field: ${searchConfig.name}`);
		}
		switch (searchConfig.type) {
			case 'value':
				this.addValueSearchRule(searchConfig as SearchValueConfig);
				break;
			case 'range':
				this.addRangeSearchRule(searchConfig as SearchRangeConfig);
				break;
			case 'list':
				this.addListSearchRule(searchConfig as SearchListConfig);
				break;
		}
	}

	private addNumericSearchRule(searchConfig: SearchConfig) {
		this.addSearchRule(searchConfig, NUMERIC_AVAILABLE_SEARCH_TYPE_LIST, 'numeric');
	}

	private addBooleanSearchRule(searchConfig: SearchConfig) {
		this.addSearchRule(searchConfig, BOOLEAN_AVAILABLE_SEARCH_TYPE_LIST, 'boolean');
	}

	private addCategoricalSearchRule(searchConfig: SearchConfig) {
		this.addSearchRule(searchConfig, CATEGORICAL_AVAILABLE_SEARCH_TYPE_LIST, 'categorical');
	}
}
