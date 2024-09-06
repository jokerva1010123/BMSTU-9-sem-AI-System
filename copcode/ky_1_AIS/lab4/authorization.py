from recommend import *
from filter import get_city_id_by_name
from read_write_data import get_data_from_json, write_data_to_json

# Max liked city Vladimir(id=4)
# Paul liked city Murom(id=16), Vologda(id=5)
# Sam liked city Zelenograd(id=7), Istra(id=10)
#	and disliked city Kaluga(id=12)

USER_FILE_PATH = "Users.json"


array_likes = []
array_dislikes = []


def load_array_likes_array_dislikes(username):
	user_data = get_data_from_json(USER_FILE_PATH)

	global array_likes, array_dislikes
	array_likes = user_data[username][0]
	array_dislikes = user_data[username][1]


def unload_array_likes_array_dislikes(username):
	user_data = get_data_from_json(USER_FILE_PATH)

	user_data[username][0] = array_likes
	user_data[username][1] = array_dislikes

	write_data_to_json(USER_FILE_PATH, user_data)


def login(username):
	load_array_likes_array_dislikes(username)

	like_cities, dislike_cities, cities = recommend(array_likes, array_dislikes)
	return like_cities, dislike_cities, cities


def get_recommend_cities():
	like_cities, dislike_cities, cities = recommend(array_likes, array_dislikes)
	return like_cities, dislike_cities, cities


def update_likes(username, city_name=None):
	like_cities, dislike_cities, cities = [], [], []
	if city_name:
		like_cities, dislike_cities, cities = add_like(username, city_name)
	else:
		like_cities, dislike_cities, cities = remove_like(username)

	return like_cities, dislike_cities, cities


def add_like(username, city_name):
	like_city_id = get_city_id_by_name(city_name)
	array_likes.append(like_city_id)
	
	like_cities, dislike_cities, cities = recommend(array_likes, array_dislikes)

	return like_cities, dislike_cities, cities


def remove_like(username):
	array_likes.pop()
	
	like_cities, dislike_cities, cities = recommend(array_likes, array_dislikes)

	return like_cities, dislike_cities, cities


def update_dislikes(username, city_name=None):
	like_cities, dislike_cities, cities = [], [], []
	if city_name:
		like_cities, dislike_cities, cities = add_dislike(username, city_name)
	else:
		like_cities, dislike_cities, cities = remove_dislike(username)

	return like_cities, dislike_cities, cities


def add_dislike(username, city_name):
	dislike_city_id = get_city_id_by_name(city_name)
	array_dislikes.append(dislike_city_id)

	like_cities, dislike_cities, cities = recommend(array_likes, array_dislikes)

	return like_cities, dislike_cities, cities


def remove_dislike(username):
	if (len(array_dislikes) > 0):
		array_dislikes.pop()
	
	like_cities, dislike_cities, cities = recommend(array_likes, array_dislikes)

	return like_cities, dislike_cities, cities


def logout(username):
	unload_array_likes_array_dislikes(username)
