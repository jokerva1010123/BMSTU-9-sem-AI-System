import json

THEMES = ['hard-gangsta', 'workout', 'soft-gangsta', 'feelings', 'fun', 'art', 'conscious']


# ox - новизна
# oy - агрессия
# oz - популярность
# сначала старые, неагрессивные, непопулярные сейчас
#a = ['Лигалайз', 'Многоточие', 'KREC', 'Гуф', 'Баста', 'Каста', 'АК-47', 'Каспийский груз', 'Кровосток', 'The Chemodan', 'Рем Дигга', 'Смоки МО', 'Миша Маваши', 'D-MAN 55', 'Грот', 'Полумягкие', 'ОУ-74', 'Паша Техник', 'Овсянкин', 'SID', 'REDO', 'RAM', 'Соня Мармеладова', 'Oxxxymiron', 'AlyonaAlyona', 'ЛСП', 'ATL', 'Макс Корж', 'Slava Marlow', 'PHAROH', 'Bulevard Depo', 'Mnogoznaal', 'Kizaru', 'Face',  'GONE.Fludd', 'Big Baby Tape', 'Элджей', 'Morgenshtern', 'MiyaGi & Andy Panda', 'Jah Khalib', 'Нурминский', 'HammAli & Navai', 'Rakhim', 'Егор Крид', 'Тимати', 'Pyrokinesis', 'ST', 'T-Fest', 'LIZER', 'Джизус', 'МУККА', 'LIDA', 'Скриптонит', 'Noize MC', 'Loqiemean', 'Anacondaz', '25/17']
# soft classic gangsta workout
# grime rapcore underground
# cloud electro vocal raprock emo mumble
# pop hookah
ARTISTS = [
    'Лигалайз', 'Многоточие', 'KREC',  # soft
    'Guf', 'Баста', 'Каста',  # classic
    'АК-47', 'Каспийский груз', 'Кровосток', 'The Chemodan', 'Смоки МО', 'Рем Дигга',  # gangsta
    'Миша Маваши', 'D-MAN 55', 'Грот',  # workout
    'Oxxxymiron', 'Соня Мармеладова', 'Alyona Alyona',  # grime
    'SID', 'REDO', 'RAM',  # rapcore
    'Полумягкие', 'ОУ74', 'Паша Техник', 'Овсянкин',  # underground
    'PHARAOH', 'Boulevard Depo', 'Mnogoznaal', 'Kizaru',  # cloud
    'ЛСП', 'ATL', 'Макс Корж', 'Slava Marlow',  # electro vocal
    'Скриптонит', 'Noize MC', 'Loqiemean', '25/17', 'Anacondaz',  # RapRock
    'LIZER', 'Джизус', 'МУККА', 'LIDA',  # emo
    'Face', 'GONE.Fludd', 'Big Baby Tape', 'Элджей', 'Morgenshtern',  # mumble
    'Rakhim', 'Егор Крид', 'Тимати', 'Pyrokinesis', 'ST', 'T-Fest',  # pop
    'MiyaGi', 'Jah Khalib', 'HammAli & Navai'  # hookah
]

ARTISTS = list(map(str.lower, ARTISTS))

leafs = ['Freestyle', 'Regular', 'Emo', 'RapRock', 'Cloud', 'Club', 'Drill', 'ElectronicVocal', 'Grime', 'Mumble', 'Phonk', 'Hardcore', 'Horrorcore', 'Underground', 'Hookah', 'Pop', 'Gangsta', 'WorkOut', 'Classic', 'Soft']
leafs = list(map(str.lower, leafs))

# матрица смежности {{'name1': 'name', 'name2': "name", "val": 10},...}


if __name__ == '__main__':
    # artists = {}
    # for leaf in leafs:
    #     artists.update({leaf: {'artist': {
    #         "year_of_birth": 1000,
    #         "group_members_num": 1,
    #         "theme": 'theme',
    #         "is_male": True,
    #     }}})
    #
    print(ARTISTS)


