import os
import itertools
import numpy as np
import pandas as pd
from tabulate import tabulate

from read_write_data import load_data
from measures import *

limit = 5

def get_measures_for_city(data_fact, like_city_id):
	city = data_fact.iloc[like_city_id]
	measures = []

	num_cities = data_fact.shape[0]
	for i in range(num_cities):
		if (i == like_city_id):
			continue
		cur_city = data_fact.iloc[i]

		measure = Minkowski_measure(0.5, city, cur_city)
		measures.append([measure, i])

	measures.sort()
	return measures[:limit]


def get_measures_by_rating(data_fact, array_rating):
	measures = []
	for rating in array_rating:
		cur_measures = get_measures_for_city(data_fact, rating)

		if (not measures):
			measures = cur_measures
		else:
			for i in range(len(measures)):
				measures[i] = measures[i] if measures[i][0] < cur_measures[i][0] else cur_measures[i]

	return measures


def match_data_with_fact_data(data, measures):
	cities = []
	for i in range(len(measures)):
		cur_idx = measures[i][1]
		cities.append(data.iloc[cur_idx])

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


def recommend_by_array_likes_dislikes(array_likes, array_dislikes):
	data, nodes, data_fact = load_data()

	like_measures = get_measures_by_rating(data_fact, array_likes)
	dislike_measures = get_measures_by_rating(data_fact, array_dislikes)
	
	dislike_max_measure = dislike_measures[-1]
	for i in range(len(dislike_measures)):
		dislike_measures[i][0] = dislike_max_measure[0] - dislike_measures[i][0]

	#measures = like_measures + dislike_measures
	measures = like_measures

	cities = match_data_with_fact_data(data, measures)

	like_cities = []
	for like in array_likes:
		like_city = data.iloc[like]
		like_cities.append(like_city)

	dislike_cities = []
	for dislike in array_dislikes:
		dislike_city = data.iloc[dislike]
		dislike_cities.append(dislike_city)

	return like_cities, dislike_cities, cities
