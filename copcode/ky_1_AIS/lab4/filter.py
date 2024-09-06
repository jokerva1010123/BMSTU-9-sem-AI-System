from read_write_data import load_data

def init_cities(data, num_cities):
	cities = []

	for i in range(num_cities):
		cities.append(data.iloc[i])

	return cities


def get_city_id_by_name(city_name):
	data, nodes, data_fact = load_data()
	idx = -1

	num_cities = data.shape[0]
	for i in range(num_cities):
		cur_city = data.iloc[i]
		if cur_city['Город'] == city_name:
			idx = i
			break

	return idx


def get_city_by_name(data, name):
	res_city = None

	num_cities = data.shape[0]
	for i in range(num_cities):
		cur_city = data.iloc[i]
		if cur_city['Город'] == name:
			res_city = cur_city
			break

	return res_city


def get_cities_by_theme(full_cities, theme):
	res_cities = []

	for city in full_cities:
		if city['Тематика'] == theme:
			res_cities.append(city)

	return res_cities


def get_cities_by_ring(full_cities, ring):
	res_cities = []

	for city in full_cities:
		if city['ЗК'] == ring:
			res_cities.append(city)

	return res_cities


def get_cities_by_distance(full_cities, distance):
	res_cities = []
	low_dist, high_dist = 0, 10000

	if distance == 'До 100 км': high_dist = 100
	if distance == '100 - 200': low_dist, high_dist = 100, 200
	if distance == '200 - 500': low_dist, high_dist = 200, 500
	if distance == 'Более 500 км': low_dist = 500

	for city in full_cities:
		if city['Расстояние от Москвы'] > low_dist and city['Расстояние от Москвы'] < high_dist:
			res_cities.append(city)

	return res_cities


def define_similar_theme(theme):
	similar_theme = theme

	if theme == "Пляжный отдых": similar_theme = "Гастрономия"
	if theme == "Гастрономия": similar_theme = "Пляжный отдых"
	if theme == "Промысел": similar_theme = "Гастрономия"
	if theme == "История": similar_theme = "Паломничество"
	if theme == "Паломничество": similar_theme = "История"

	return similar_theme


def get_cities_by_another_filter(data, theme, in_ring, out_ring, distance):
	cities = init_cities(data, data.shape[0])

	if theme != 'Тематика':
		theme = define_similar_theme(theme)
		cities = get_cities_by_theme(cities, theme)

	if in_ring:
		cities = get_cities_by_ring(cities, '+')

	if out_ring:
		cities = get_cities_by_ring(cities, '-')

	if distance != 'Расстояние от Москвы':
		cities = get_cities_by_distance(cities, distance)

	return cities


def find_cities_by_filters(name, theme, in_ring, out_ring, distance):
	data, nodes, data_fact = load_data()
	another_filter = False

	if name:
		city = get_city_by_name(data, name)
		cities = [city]
		return cities, another_filter

	cities = init_cities(data, data.shape[0])

	if theme != 'Тематика':
		cities = get_cities_by_theme(cities, theme)

	if in_ring:
		cities = get_cities_by_ring(cities, '+')

	if out_ring:
		cities = get_cities_by_ring(cities, '-')

	if distance != 'Расстояние от Москвы':
		cities = get_cities_by_distance(cities, distance)

	if len(cities) == 0:
		another_filter = True
		cities = get_cities_by_another_filter(data, theme, in_ring, out_ring, distance)

	return cities, another_filter
