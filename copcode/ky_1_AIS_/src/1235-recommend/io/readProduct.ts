import {readUntil} from './readUntil';


export const readNaturalOrZeroNumberOf = (what: string, maximum: number): number =>
	Number(
		readUntil(
			`Input number of ${what}: `,
			`There is no such number of products (available: ${maximum})`,
			(input: string): boolean => {
				const n = Number(input);
				return !isNaN(n) && Number.isInteger(n) && (0 <= n && n <= maximum);
			}
		)
	);

export const readProduct = (productNumber: string, products: string[]): string =>
	readUntil(
		`Input ${productNumber} product: `,
		'There is no such product',
		(product: string): boolean =>
			products.includes(product)
	);

export const readProducts = (ofWhat: string, products: string[]): string[] =>
	Array.from(
		{length: readNaturalOrZeroNumberOf(ofWhat, products.length)},
		(value: number, index: number): string =>
			readProduct(`${index + 1}`, products)
	);
