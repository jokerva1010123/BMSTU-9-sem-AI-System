from collections import OrderedDict
from lab5.src.recommender_system.interface import find_artist

EXCLUDE = ['sex', 'group_type', 'older', 'younger']


def loosen_filters(filtered_recommendations, values, recommendations):
    i = 0
    exclude = []
    while not filtered_recommendations and i < len(EXCLUDE):
        exclude.append(EXCLUDE[i])
        filtered_recommendations = filter_(parse_filters(values), recommendations, exclude=exclude)
        i += 1
    return filtered_recommendations


def filter_(filters, recommendations, exclude=None):
    exclude = exclude if exclude else []
    filtered_recommendations = OrderedDict()
    group_type = filters['group_type']
    sex = filters['sex']
    older = int(filters['older']) if filters['older'] else None
    younger = int(filters['younger']) if filters['younger'] else None
    for artist_name, proximity in recommendations.items():
        artist = find_artist(artist_name)
        if group_type != 'any' and artist.solo_duet_group != group_type and 'group_type' not in exclude:
            continue
        if sex != 'anysex' and artist.sex != sex and 'sex' not in exclude:
            continue
        if older and artist.age <= older and 'older' not in exclude:
            continue
        if younger and artist.age >= younger and 'younger' not in exclude:
            continue
        if artist_name not in filtered_recommendations:
            filtered_recommendations.update({artist_name: proximity})
    return filtered_recommendations


def parse_filters(values) -> dict:
    filters = {}
    for sex in ['_male_', '_female_', '_any_sex_']:
        if values[sex]:
            filters['sex'] = sex.replace('_', '')
            break

    for group_type in ['_solo_', '_duet_', '_group_', '_any_']:
        if values[group_type]:
            filters['group_type'] = group_type.replace('_', '')
            break

    filters['older'] = values['_older_']
    filters['younger'] = values['_younger_']

    return filters


def trunc_result(recommendations: OrderedDict, max_result_len: int):
    if max_result_len:
        limited_recommendations = OrderedDict()
        i = 0
        for key, val in recommendations.items():
            if i >= max_result_len:
                break
            i += 1
            limited_recommendations.update({key: val})
        return limited_recommendations