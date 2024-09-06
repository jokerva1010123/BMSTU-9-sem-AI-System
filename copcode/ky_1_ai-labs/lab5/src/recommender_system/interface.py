import os
from collections import OrderedDict
from lab5.src.recommender_system.recommendation_list import get_recommendations
from lab5.src.recommender_system.recommendation_list import (
    Node, create_tree_from_json, load_artist_pairs_proximity_json, calc_max_general_proximity,
    calc_min_general_proximity, normalize_proximities)
from lab5.src.recommender_system.tree.tree_tools import calc_max_distance_between_nodes
from lab5.src.recommender_system.tree.genre_node import GenreVisualNode

dir_path = os.path.dirname(os.path.realpath(__file__))
TREE = create_tree_from_json(f'{dir_path}/data/genres.json')
ARTIST_PAIRS_PROXIMITY = load_artist_pairs_proximity_json()
max_proximity = calc_max_general_proximity(ARTIST_PAIRS_PROXIMITY)
min_proximity = calc_min_general_proximity(ARTIST_PAIRS_PROXIMITY)
max_distance_between_nodes = calc_max_distance_between_nodes(TREE)
normalize_proximities(ARTIST_PAIRS_PROXIMITY, min_proximity, max_proximity)


class ParseError(Exception): pass
class ArgumentError(Exception): pass


def find_artist(name: str) -> GenreVisualNode:
    artist = Node.get_child_by_name(TREE, name)
    if not artist:
        raise ArgumentError(f'Артиста "{name}" нет в базе')
    return artist


def split_artists(artists: str):
    artists.strip()
    artists = artists.replace('  ', ' ')
    artists = artists.replace('   ', ' ')
    res = list(map(str.strip, artists.split(',')))
    return res


def recommend_by_seed(seed_artist: str):
    seed = find_artist(seed_artist)
    return get_recommendations(seed, ARTIST_PAIRS_PROXIMITY)


def recommend_by_liked(liked_artist_names: str):
    liked_artist_names_list = split_artists(liked_artist_names)
    liked_artists = {find_artist(artist.lower()) for artist in liked_artist_names_list}

    artist_recommendations = OrderedDict()
    for artist in liked_artists:
        recommendations = get_recommendations(
            artist,
            ARTIST_PAIRS_PROXIMITY
        )
        artist_recommendations[artist.name] = \
            [(artist_name, proximity) for artist_name, proximity in recommendations.items()]

    final_recommendations = {}
    max_recommendation_len = max(map(len, artist_recommendations.values()))
    for i in range(max_recommendation_len):
        for artist, recommendations in artist_recommendations.items():
            if len(recommendations) > i:
                name = recommendations[i][0]
                proximity = recommendations[i][1]
                if name not in final_recommendations and name not in liked_artist_names_list:
                    final_recommendations[name] = proximity

    final_recommendation_artists = list(final_recommendations.keys())
    final_dict = OrderedDict({artist: final_recommendations[artist] for artist in final_recommendation_artists})

    return final_dict


def recommend_by_liked_with_disliked(disliked_artists: str, liked_artist_names: str, debug=False):
    recommendations_by_liked = recommend_by_liked(liked_artist_names)
    disliked_artists = split_artists(disliked_artists)
    for dislike in disliked_artists:
        if dislike in recommendations_by_liked:
            recommendations_by_liked.pop(dislike)
            if debug:
                print(f'Артист {dislike} удалён из выборки')
    return recommendations_by_liked


