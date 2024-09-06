import PySimpleGUI as sg
import interface
from data.artists import ARTISTS

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
        sg.InputText(key='_seed_'),
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
    [sg.Checkbox('Очищать вывод', default=True, key='_clean_output_'), sg.Checkbox('DEBUG', default=True, key='_debug_')],
    [sg.Button('Очистить поля ввода')],
    [
        sg.Output(size=(80, 20), key='_output_'),
        sg.Text(size=(18, 30), key='_artists_', text=available_artists1),
        sg.Text(size=(18, 30), key='_artists_', text=available_artists2)
    ],
    [sg.Submit(button_text='Рекомендовать'), sg.Cancel()]
]


def show():
    window = sg.Window('lab3', layout)
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
                if clean:
                    window['_output_'].Update('')
                try:
                    interface.recommend_by_seed(seed, max_len)
                except interface.ParseError as e:
                    print('Не могу разобрать аргументы')
                    print(e)
                except interface.ArgumentError as e:
                    print(e)
                except Exception as e:
                    print(f'Неизвестная ошибка: {e}')
            elif use_disliked:
                if clean:
                    window['_output_'].Update('')
                try:
                    interface.recommend_by_disliked(disliked, liked, max_len, debug)
                except interface.ParseError:
                    print('Не могу разобрать аргументы')
                except Exception as e:
                    print(f'Неизвестная ошибка: {e}')
            elif liked_radio:
                if clean:
                    window['_output_'].Update('')
                try:
                    interface.recommend_by_liked(liked, max_len)
                except interface.ParseError:
                    print('Не могу разобрать аргументы')
                except interface.ArgumentError as e:
                    print(e)
                except Exception as e:
                    print(f'Неизвестная ошибка: {e}')


    window.close()
