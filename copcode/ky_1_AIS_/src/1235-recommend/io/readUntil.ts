import * as readlineSync from 'readline-sync';


export const readUntil = (prompt: string, error: string, callback: (string) => boolean): string => {
	let value = "";
	while (true) {
		value = readlineSync.question(prompt);
		if (callback(value)) {
			break;
		}
		console.error(error);
	}
	return value;
};
