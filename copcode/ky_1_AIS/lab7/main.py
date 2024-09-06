import pymorphy2
import re

from answer import *
from cities import *

morph = pymorphy2.MorphAnalyzer()

attributes = [["Город", "название", "\nНапиши название."], 
				["Тематика", "тематика", "\nУкажи тематику."], 
				["Вид промысла", "промысел", "\nУкажи вид промысла."], 
				["Историческая эпоха", "история", "\nУкажи историческую эпоху."], 
				["Историческая личность", "личность", "\nУкажи историческую личность."],
				["ЗК", "зк", "\nВходит в золотое кольцо?"]]
selected_attributes = ''

step = 0
scenarios = -1

def handle(phrase):
	global step, scenarios, attributes, selected_attributes
	
	if len(set(phrase) & {'давать', 'привет', 'добрый', 'здравствуй', 'здравствуйте'}) != 0:
		welcome()
		return

	if len(set(phrase) & {'пока', 'нет'}) != 0:
		bye()
		exit(0)

	if (len(set(phrase) & {'какой', 'вывести', 'показать', 'написать', 'перечислить', 'список', 'подсказать'}) != 0
		and len(set(phrase) & {'всё' , 'все', 'перечень', 'каталог', 'список'}) != 0
		and len(set(phrase) & {'город'}) != 0):
		
		full_list()
		return

	if (len(set(phrase) & {'случайный', 'любой', 'какойнибудь'}) != 0):
		random_city()
		return

	if (len(set(phrase) & {'близко', 'близкий', 'далеко', 'далёкий', 'средне', 'средний', 'очень', 'не'}) != 0):
		distance_city(phrase)
		more()
		return

	if (len(set(phrase) & {'какой', 'вывести', 'показать', 'найти', 'подсказать'}) != 0
				and len(set(phrase) & {'город'}) != 0) or scenarios >= 3:
		if scenarios == -1:
			scenarios = 3

		if step == 0:
			print('\nПоказать город по названию?')
			string = input()
			string_parser = parser(string)

			if ('да') in string_parser:
				step = 2
				scenarios = 4
				
				print('\nЧто за город?')
				city_title = input()
				
				step = 0
				scenarios = -1

				city = find_city(city_title)
				if city == -1:
					not_found()
				else:
					more()

			elif 'нет' in string_parser:
				step = 2
				scenarios = 5
				
				print('\nПо какому критерию будем искать?')
			else:
				step = 0
				scenarios = -1

				print(string)
				city = find_city(city_title)
				if city == -1:
					not_found()
				else:
					more()
			return

		elif step == 2:
			if scenarios == 5:
				attr = ''
				for i in range(len(attributes)):
					
					if attributes[i][1].lower() in set(phrase):
						attr = attributes[i][0]
						selected_attributes = attributes[i][0]
						print(attributes[i][2])
						step = 3
						scenarios = 5
				
				if attr == '':
					print('\nУверен, что не опечатался?')
		
		elif step == 3:
			step = 0
			scenarios = -1

			output_cities(phrase, selected_attributes)
			more()

	else:
		not_found()
		more()
	
	return


def parser(s):
	phrase = re.sub(r'[^\w\s]', '', s.lower()).split()
	norm_phrase = list()
	for word in phrase:
		norm_phrase.append(morph.parse(word)[0].normal_form)
	return norm_phrase

  
def main():
	welcome()

	while True:
		phrase = input()
		norm_phrase = parser(phrase)
		#print(norm_phrase)
		handle(norm_phrase)

if __name__ == "__main__":
	main()