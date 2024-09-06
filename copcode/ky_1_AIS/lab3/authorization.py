from recommend import *

# Max liked city Vladimir(id=4)
# Paul liked city Murom(id=16), Vologda(id=5)
# Sam liked city Zelenograd(id=7), Istra(id=10)
#	and disliked city Kaluga(id=12)

def login(user_name):
	like_cities, dislike_cities, cities = [], [], []

	if user_name == "Max":
		like_cities, cities = recommend_by_like(4)
	elif user_name == "Paul":
		like_cities, cities = recommend_by_array_likes([5, 12])
	elif user_name == "Sam":
		like_cities, dislike_cities, cities = recommend_by_array_likes_dislikes([7, 10], [24])

	return like_cities, dislike_cities, cities
