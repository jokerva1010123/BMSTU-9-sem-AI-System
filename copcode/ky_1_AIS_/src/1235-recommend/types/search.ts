export type SearchValueConfig = {
	name: string,
	type: 'value',
	value: number,
};

export type SearchRangeConfig = {
	name: string,
	type: 'range',
	min: number,
	max: number,
}

export type SearchListConfig = {
	name: string,
	type: 'list',
	list: string[],
};

export type SearchConfig = SearchValueConfig | SearchRangeConfig | SearchListConfig;
