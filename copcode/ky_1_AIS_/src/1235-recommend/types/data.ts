import {simpleDeepCopy} from '../algorithms/copy';

export type InodeData = {
	name: string,
}

export type LeafData = {
	name: string,
	volume: number,
	price: number,
	abv: number,
	age: number,
	country: string,
	carbonated: boolean,
	mainTaste: 'bitter' | 'sour' | 'sweet',
};

export const LEAF_DATA_NUMERIC_FIELDS = ['volume', 'price', 'abv', 'age'];
export const LEAF_DATA_BOOLEAN_FIELDS = ['carbonated'];
export const LEAF_DATA_CATEGORICAL_FIELDS = [
	{
		name: 'mainTaste',
		values: ['bitter', 'sour', 'sweet'],
	},
];

type NormalizedLeafData = {
	volume: number,
	price: number,
	abv: number,
	age: number,
	carbonated: number,
	mainTaste: number,
};

type Score = {
	like: number,
	dislike: number,
	total: number,
}

export class ExtendedLeafData {
	source: LeafData = {
		name: '__noname__',
		volume: 0,
		price: 0,
		abv: 0,
		age: 0,
		country: '__no_country__',
		carbonated: false,
		mainTaste: 'bitter',
	};
	path: string[] = [];
	normalized: NormalizedLeafData = {
		volume: 0.5,
		price: 0.5,
		abv: 0.5,
		age: 0.5,
		carbonated: 0.5,
		mainTaste: 0.5,
	};
	score: Score = {
		like: 0,
		dislike: 0,
		total: 0,
	};

	constructor(leafData?: LeafData) {
		if (typeof leafData === 'undefined') {
			return;
		}

		this.source = simpleDeepCopy(leafData);

		LEAF_DATA_NUMERIC_FIELDS.forEach((field: string) => {
			this.normalized[field] = leafData[field];
		});
		LEAF_DATA_BOOLEAN_FIELDS.forEach((field: string) => {
			this.normalized[field] = Number(leafData[field]);
		});
		LEAF_DATA_CATEGORICAL_FIELDS.forEach(({name, values}) => {
			this.normalized[name] = values.indexOf(leafData[name]) / (values.length - 1);
		});
	}
}

export const EXTENDED_LEAF_DATA_NORMALIZED_FIELDS =
	LEAF_DATA_NUMERIC_FIELDS
		.concat(LEAF_DATA_BOOLEAN_FIELDS)
		.concat(
			LEAF_DATA_CATEGORICAL_FIELDS
				.map(field => field.name)
		);

export const EXTENDED_LEAF_DATA_NORMALIZED_FIELDS_WEIGHTS = {
	volume: 1.1,
	price: 1.5,
	abv: 1.5,
	age: 0.8,
	carbonated: 0.7,
	mainTaste: 0.4,
};
