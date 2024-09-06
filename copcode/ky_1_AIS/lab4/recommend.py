import os
import itertools
import numpy as np
import pandas as pd
from tabulate import tabulate

from read_write_data import load_data
from measures import *

limit = 6

def get_measures_for_city(data_fact, rating, array_rating, array_disrating):
	city = data_fact.iloc[rating]
	measures = []

	num_cities = data_fact.shape[0]
	for i in range(num_cities):
		if (i in array_rating or i in array_disrating):
			continue
		cur_city = data_fact.iloc[i]

		measure = Minkowski_measure(0.5, city, cur_city)
		measures.append([measure, i])

	measures.sort()
	return measures


def get_measures_by_rating(data_fact, array_rating, array_disrating):
	measures = []
	for rating in array_rating:
		cur_measures = get_measures_for_city(data_fact, rating, array_rating, array_disrating)

		if (not measures):
			measures = cur_measures
		else:
			for i in range(len(measures)):
				if measures[i][0] > cur_measures[i][0]:
					measures[i] = cur_measures[i]

	return measures


def match_data_with_fact_data(data, measures):
	cities = []
	for i in range(len(measures)-1):
		cur_idx = measures[i][1]
		next_idx = measures[i+1][1]

		if cur_idx == next_idx:
			continue

		cities.append(data.iloc[cur_idx])
		
	cities.append(data.iloc[len(measures)-1])

	return cities


def recommend_by_like(like_city_id):
	data, nodes, data_fact = load_data()
	measures = get_measures_for_city(data_fact, like_city_id)
	
	cities = match_data_with_fact_data(data, measures)
	like_city = data.iloc[like_city_id]

	return [like_city], cities


def recommend_by_array_likes(array_likes):
	data, nodes, data_fact = load_data()

	measures = get_measures_by_rating(data_fact, array_likes)
	cities = match_data_with_fact_data(data, measures)
	
	like_cities = []
	for like in array_likes:
		like_city = data.iloc[like]
		like_cities.append(like_city)

	return like_cities, cities


def recommend(array_likes, array_dislikes):
	data, nodes, data_fact = load_data()

	like_measures = get_measures_by_rating(data_fact, array_likes, array_dislikes)
	dislike_measures = get_measures_by_rating(data_fact, array_dislikes, array_likes)
	
	if dislike_measures:
		dislike_max_measure = dislike_measures[-1]
		for i in range(len(dislike_measures)):
			dislike_measures[i][0] = dislike_max_measure[0] - dislike_measures[i][0]

	#measures = like_measures + dislike_measures
	measures = like_measures

	like_cities = []
	for like in array_likes:
		like_city = data.iloc[like]
		like_cities.append(like_city)

	dislike_cities = []
	for dislike in array_dislikes:
		dislike_city = data.iloc[dislike]
		dislike_cities.append(dislike_city)

	cities = match_data_with_fact_data(data, measures)

	return like_cities, dislike_cities, cities
