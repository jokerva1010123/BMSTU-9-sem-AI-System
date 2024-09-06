import * as alcoholMap from '../../docs/alcohol-map.json';
import {recommend} from './recommender/recommend';
import {LeafData, ExtendedLeafData} from './types/data';
import {TreeNode} from './types/node';
import {getLeavesData, normalizeLeavesData} from './algorithms/leaves';
import {readProducts} from './io/readProduct';


const main = () => {
	const root: TreeNode = alcoholMap;
	const leavesData: LeafData[] = getLeavesData(root);
	const extendedLeavesData: ExtendedLeafData[] = normalizeLeavesData(leavesData);
	const products: string[] = leavesData.map((leafData: LeafData): string => leafData.name);

	console.log('List of products: ', products);

	const likes = readProducts('likes', products);
	const productsMinusLikes = products.filter((product: string): boolean => !likes.includes(product));

	const dislikes = readProducts('dislikes', productsMinusLikes);

	const recommendations = recommend(root, extendedLeavesData, likes, dislikes);
	console.log(recommendations);
};

main();
