from typing import Callable, Tuple, Dict
import PySimpleGUI as sg
from lab5.src.recommender_system import filter
from lab5.src.recommender_system import interface
from lab5.src.recommender_system.data.artists import ARTISTS

artists_list = reversed(ARTISTS)
artists_list = [artist.ljust(18) for artist in artists_list]
available_artists1 = '\n'.join(list(artists_list[:30]))
available_artists2 = '\n'.join(list(artists_list[30:]))


# самые непохожие: noize mc лигалайз, alyona alyona каста, noize mc guf, noize mc баста, noize mc лигалайз
# самые похожие: ram sid, баста guf, krec многоточие

layout = [
    [
        sg.Text('Рекомендация по затравочному значению', size=(39, 1)),
        sg.Radio(text='', group_id=0, default=True, key='_seed_radio_'),
        sg.InputText(key='_seed_', default_text='кровосток'),
    ],
    [
        sg.Text('Рекомендация по списку лайков (через запятую)', size=(39, 1)),
        sg.Radio(text='', group_id=0, key='_liked_radio_'),
        sg.InputText(key='_liked_', default_text='noize mc, лигалайз, guf')
    ],
    [
        sg.Text('Учитывать дизлайки', size=(39, 1)),
        sg.Checkbox(text='', key='_dislikes_'),
        sg.InputText(key='_disliked_', default_text='jah khalib, t-fest, hammali & navai')
    ],
    [
        sg.Text('Сколько артистов выводить (число или "all"):', size=(33, 1)),
        sg.InputText(default_text='6', key='_max_len_', size=(5, 1))
    ],
    [
        sg.Text('Фильтры: ')
    ],
    [
        sg.Radio(text='male', group_id=1, key='_male_'), sg.Radio(text='female', group_id=1, key='_female_'),
        sg.Radio(text='any_sex', group_id=1, default=True, key='_any_sex_'),
        sg.Text('|'),
        sg.Radio(text='solo', group_id=2, key='_solo_'), sg.Radio(text='duet', group_id=2, key='_duet_'),
        sg.Radio(text='group', group_id=2, key='_group_'),
        sg.Radio(text='any', group_id=2, default=True, key='_any_'),
        sg.Text('|'),
        sg.Text('Старше чем (лет): '), sg.InputText(key='_older_', size=(5, 1)),
        sg.Text('Младше чем (лет): '), sg.InputText(key='_younger_', size=(5, 1)),
    ],
    [sg.Checkbox('Очищать вывод', default=True, key='_clean_output_'), sg.Checkbox('DEBUG', default=True, key='_debug_')],
    [sg.Button('Очистить поля ввода')],
    [
        sg.Output(size=(80, 20), key='_output_'),
        sg.Text(size=(18, 30), key='_artists_', text=available_artists1),
        sg.Text(size=(18, 30), key='_artists_', text=available_artists2)
    ],
    [sg.Submit(button_text='Рекомендовать'), sg.Cancel()]
]


def print_recommendations(recommendations, max_output_len, debug=False):
    for i, artist_name in enumerate(recommendations):
        if i < max_output_len:
            if debug:
                print(artist_name, recommendations[artist_name])
            else:
                print(artist_name)


def handle_command(
        window,
        values: Dict,
        max_output_len: int,
        clean: bool,
        debug: bool,
        recommend_handler: Callable,
        handler_args: Tuple = tuple(),
        handler_kwargs: Dict = None):
    if clean:
        window['_output_'].Update('')
    try:
        handler_kwargs = dict() if not handler_kwargs else handler_kwargs
        recommendations = recommend_handler(*handler_args, **handler_kwargs)
        filtered_recommendations = filter.filter_(filter.parse_filters(values), recommendations)
        if not filtered_recommendations:
            print('Не найдено точного соответствия, однако, возможно, вам понравится:')
            filtered_recommendations = filter.loosen_filters(filtered_recommendations, values, recommendations)
        print_recommendations(filtered_recommendations, max_output_len, debug)

    except interface.ParseError as e:
        print('Не могу разобрать аргументы')
        print(e)
    except interface.ArgumentError as e:
        print(e)
    except Exception as e:
        print(f'Неизвестная ошибка: {e}')


def show():
    window = sg.Window('RK1', layout)
    while True:
        event, values = window.read()
        seed = values['_seed_']
        seed_radio = values['_seed_radio_']
        liked = values['_liked_']
        liked_radio = values['_liked_radio_']
        disliked = values['_disliked_']
        use_disliked = values['_dislikes_']
        max_len = 100 if values['_max_len_'].lower() == 'all' else int(values['_max_len_'])
        clean = values['_clean_output_']
        debug = values['_debug_']
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Очистить поля ввода':
            window['_seed_'].Update('')
            window['_liked_'].Update('')
            window['_disliked_'].Update('')
        if event == 'Рекомендовать':
            if seed_radio:
                handle_command(window, values, max_len, clean, debug, interface.recommend_by_seed, (seed,))
            elif use_disliked:
                handle_command(window, values, max_len, clean, debug,
                               interface.recommend_by_liked_with_disliked, (disliked, liked, debug))
            elif liked_radio:
                handle_command(window, values, max_len, clean, debug, interface.recommend_by_liked, (liked,))

    window.close()

