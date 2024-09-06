import * as alcoholMap from '../../docs/alcohol-map.json';
import * as searchConfigJson from '../../docs/search-config.json';
import {ApproxSearchEngine} from './search/approx';
import {LeafData, ExtendedLeafData} from './types/data';
import {TreeNode} from './types/node';
import {getLeavesData, normalizeLeavesData} from './algorithms/leaves';
import {SearchConfig} from './types/search';
import {SearchEngine} from './search/search';


// 0.33 - 1
// 130 - 9800
// 4 - 40
// 1 - 12
// 'bitter' | 'sour' | 'sweet'

const main = () => {
	const root: TreeNode = alcoholMap;
	const leavesData: LeafData[] = getLeavesData(root);
	const extendedLeavesData: ExtendedLeafData[] = normalizeLeavesData(leavesData);

	const searchConfigs: SearchConfig[] = searchConfigJson as SearchConfig[];
	console.log(searchConfigs);
	const searchEngine: SearchEngine = new SearchEngine(searchConfigs);

	const searchResults = searchEngine.findAll(extendedLeavesData);
	if (!searchResults.length) {
		const LIMIT = 5;
		const approxSearchEngine = new ApproxSearchEngine(searchConfigs, leavesData);
		console.log('=== Не найдено точного соответствия, однако, возможно, Вам понравится:');
		console.log(approxSearchEngine.findAll(root, extendedLeavesData).slice(0, LIMIT));
		return;
	}
	console.log('===  Найдено:');
	console.log(searchResults);
};

main();
