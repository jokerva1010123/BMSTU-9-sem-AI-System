import {simpleDeepCopy} from '../algorithms/copy';
import {calculateCustomDistance} from '../metrics/custom';
import {ExtendedLeafData} from '../types/data';
import {TreeNode} from '../types/node';


export const recommendByOne = (root: TreeNode, __extendedLeavesData: ExtendedLeafData[], product: string) => {
	const workingLeavesData: ExtendedLeafData[] = simpleDeepCopy(__extendedLeavesData);
	const [origin] = workingLeavesData.splice(
		workingLeavesData.findIndex(
			(workingLeafData: ExtendedLeafData) =>
				workingLeafData.source.name === product
		),
		1
	);

	workingLeavesData.forEach((workingLeafData: ExtendedLeafData) => {
		workingLeafData.score.like = calculateCustomDistance(root, workingLeafData, origin);
		workingLeafData.score.total = workingLeafData.score.like;
	});

	return workingLeavesData.sort((lhs: ExtendedLeafData, rhs: ExtendedLeafData): number => lhs.score.total - rhs.score.total);
};

export const recommend = (root: TreeNode, __extendedLeavesData: ExtendedLeafData[], likes: string[], dislikes: string[]) => {
	let workingLeavesData: ExtendedLeafData[] = simpleDeepCopy(__extendedLeavesData);
	const likesData = workingLeavesData.filter(workingLeafData => likes.includes(workingLeafData.source.name));
	workingLeavesData = workingLeavesData.filter(workingLeafData => !likes.includes(workingLeafData.source.name));
	const dislikesData = workingLeavesData.filter(workingLeafData => dislikes.includes(workingLeafData.source.name));
	workingLeavesData = workingLeavesData.filter(workingLeafData => !dislikes.includes(workingLeafData.source.name));

	workingLeavesData.forEach(
		(workingLeafData: ExtendedLeafData) => {
			workingLeafData.score.like = Math.min(
				...likesData.map(
					likeData => calculateCustomDistance(root, workingLeafData, likeData)
				)
			);
			workingLeafData.score.dislike = Math.min(
				...dislikesData.map(
					dislikeData => calculateCustomDistance(root, workingLeafData, dislikeData)
				)
			);
		}
	);

	const maxDislikeScore = 2;
	workingLeavesData = workingLeavesData.sort(
		(lhs: ExtendedLeafData, rhs: ExtendedLeafData): number =>
			rhs.score.dislike - lhs.score.dislike
	);

	workingLeavesData.forEach(
		(workingLeafData: ExtendedLeafData, i: number) => {
			workingLeafData.score.dislike =
				dislikes.length
					? i * maxDislikeScore / (workingLeavesData.length - 1)
					: 0;
			workingLeafData.score.total = workingLeafData.score.like + workingLeafData.score.dislike;
		}
	);

	return workingLeavesData.sort(
		(lhs: ExtendedLeafData, rhs: ExtendedLeafData): number =>
			lhs.score.total - rhs.score.total
	);
};
