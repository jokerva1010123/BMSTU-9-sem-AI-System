import * as alcoholMap from '../../docs/alcohol-map.json';
import * as readlineSync from 'readline-sync';
import * as fs from 'fs';
import {simpleDeepCopy} from "./algorithms/copy";
import {readNaturalOrZeroNumberOf, readProducts} from "./io/readProduct";
import {recommend} from "./recommender/recommend";
import {ApproxSearchEngine} from './search/approx';
import {LeafData, ExtendedLeafData} from './types/data';
import {TreeNode} from './types/node';
import {getLeavesData, normalizeLeavesData} from './algorithms/leaves';
import {SearchConfig} from './types/search';
import {SearchEngine} from './search/search';


class RK1 {
	root: TreeNode;
	leavesData: LeafData[];
	extendedLeavesData: ExtendedLeafData[];
	workingLeavesData: ExtendedLeafData[];

	constructor(root: TreeNode) {
		this.root = root;
		this.leavesData = getLeavesData(root);
		this.extendedLeavesData = normalizeLeavesData(this.leavesData);
		this.workingLeavesData = simpleDeepCopy(this.extendedLeavesData);
	}

	run() {
		while (true) {
			console.log('0. Reset All');
			console.log('1. Recommend (LAB 3)');
			console.log('2. Search (LAB 5)');
			console.log('3. Quit');
			const n = readNaturalOrZeroNumberOf('menu', 3);
			switch (n) {
				case 0:
					this.reset();
					break;
				case 1:
					this.recommend();
					break;
				case 2:
					this.search();
					break;
				case 3:
					console.log('Good bye!');
					process.exit();
			}
		}
	}

	reset() {
		this.workingLeavesData = simpleDeepCopy(this.extendedLeavesData);
		console.clear();
	}

	recommend() {
		const products: string[] = this.workingLeavesData.map((leafData: ExtendedLeafData): string => leafData.source.name);
		console.log('List of products: ', products);

		const likes = readProducts('likes', products);
		const productsMinusLikes = products.filter((product: string): boolean => !likes.includes(product));

		const dislikes = readProducts('dislikes', productsMinusLikes);

		const recommendations = recommend(this.root, this.workingLeavesData, likes, dislikes);
		const n = readNaturalOrZeroNumberOf('out recommendations', recommendations.length);
		this.workingLeavesData = recommendations.slice(0, n);
		console.log(this.workingLeavesData);
	}

	search() {
		readlineSync.question('Change search-config.json and press any key to search');
		const searchConfigs: SearchConfig[] = JSON.parse(fs.readFileSync('./docs/search-config.json').toString());
		console.log(searchConfigs);
		const searchEngine: SearchEngine = new SearchEngine(searchConfigs);

		const searchResults = searchEngine.findAll(this.workingLeavesData);
		if (!searchResults.length) {
			const approxSearchEngine = new ApproxSearchEngine(searchConfigs, this.leavesData);
			console.log('========== No exact match found, however you may like :');
			const n = readNaturalOrZeroNumberOf('out recommendations', this.workingLeavesData.length);
			this.workingLeavesData = approxSearchEngine.findAll(this.root, this.workingLeavesData).slice(0, n);
			console.log(this.workingLeavesData);
			return;
		}
		console.log('========== Found:');
		console.log(searchResults);
		this.workingLeavesData = searchResults;
	}
}


const main = () => {
	const root: TreeNode = alcoholMap;

	const rk1 = new RK1(root);
	rk1.run();
};

main();
