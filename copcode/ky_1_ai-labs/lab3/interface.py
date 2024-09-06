import random
from collections import OrderedDict
from recommendation_list import show_recommendations, get_recommendations
from recommendation_list import (
    Node, create_tree_from_json, load_artist_pairs_proximity_json, calc_max_general_proximity,
    calc_min_general_proximity, normalize_proximities)
from proximity_measures import generalizing_proximity_measure
from tree.tree_tools import calc_max_distance_between_nodes
from tree.genre_node import GenreVisualNode


TREE = create_tree_from_json('data/genres.json')
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


def recommend_by_seed(seed_artist: str, max_output_len=5):
    seed = find_artist(seed_artist)

    show_recommendations(seed, ARTIST_PAIRS_PROXIMITY, max_len=max_output_len)


def recommend_by_liked(liked_artist_names: str, max_output_len=5, show=True):
    liked_artist_names_list = split_artists(liked_artist_names)
    liked_artists = {find_artist(artist.lower()) for artist in liked_artist_names_list}

    artist_recommendations = OrderedDict()
    for artist in liked_artists:
        recommendations = get_recommendations(
            artist,
            ARTIST_PAIRS_PROXIMITY
        )
        artist_recommendations[artist.name] = recommendations

    final_recommendations = {}
    max_artists_recommendations_len = max_output_len // len(liked_artists)
    max_artists_recommendations_len += 1 if max_output_len % len(liked_artists) != 0 else 0
    for artist, recommendations in artist_recommendations.items():
        i = 0
        for name, proximity in recommendations.items():
            if i >= max_artists_recommendations_len:
                break
            if name not in final_recommendations:
                final_recommendations[name] = proximity
                i += 1

    final_recommendation_artists = list(final_recommendations.keys())
    random.shuffle(final_recommendation_artists)
    for i, artist_name in enumerate(final_recommendation_artists):
        if i < max_output_len:
            # print(artist_name, final_recommendations[artist_name])
            if show:
                print(artist_name)
    return final_recommendation_artists


def check_artist_like_dislike(artist, dislikes, debug=True) -> bool:
    for dislike in dislikes:
        artist_dislike_proximity = generalizing_proximity_measure(TREE, artist, dislike, max_distance_between_nodes, min_proximity, max_proximity)
        if artist_dislike_proximity < 0.49:
            if debug:
                print(f'[DEBUG] {artist} похож на {dislike}: {artist_dislike_proximity}')
            return False
    return True


def recommend_by_disliked(disliked_artists: str, liked_artist_names: str, max_output_len=5, debug=True):
    liked_artist_names_list = split_artists(liked_artist_names)
    liked_artists = {find_artist(artist.lower()) for artist in liked_artist_names_list}

    artist_recommendations = OrderedDict()
    for artist in liked_artists:
        recommendations = get_recommendations(
            artist,
            ARTIST_PAIRS_PROXIMITY
        )
        artist_recommendations[artist.name] = recommendations

    disliked_artist_names_list = split_artists(disliked_artists)
    disliked_artists = {find_artist(artist.lower()) for artist in disliked_artist_names_list}
    #print(disliked_artists)

    final_recommendations = {}
    max_artists_recommendations_len = max_output_len // len(liked_artists)
    max_artists_recommendations_len += 1 if max_output_len % len(liked_artists) != 0 else 0
    for artist, recommendations in artist_recommendations.items():
        i = 0
        for name, proximity in recommendations.items():
            if i >= max_artists_recommendations_len:
                break
            recommended_artist = find_artist(name.lower())
            if name not in final_recommendations:
                if check_artist_like_dislike(recommended_artist, disliked_artists, debug):
                    final_recommendations[name] = proximity
                    i += 1

    for i, artist_name in enumerate(final_recommendations):
        if i < max_output_len:
            # print(artist_name, final_recommendations[artist_name])
            if artist_name not in disliked_artist_names_list:
                print(artist_name)
            else:
                if debug:
                    print(f'[DEBUG] Не выводим {artist_name}, тк он дизлайкнут')


def recommend_by_disliked2(disliked_artists: str, liked_artist_names: str, max_output_len=5, debug=True):
    disliked_artist_names_list = split_artists(disliked_artists)
    disliked_artists = {find_artist(artist.lower()) for artist in disliked_artist_names_list}
    #print(disliked_artists)
    final_recommendation_artists = recommend_by_liked(liked_artist_names, max_output_len, show=False)
    #print(res)
    for i, artist_name in enumerate(final_recommendation_artists):
        if i < max_output_len:
            # print(artist_name, final_recommendations[artist_name])
            if artist_name not in disliked_artist_names_list:
                print(artist_name)
            else:
                if debug:
                    print(f'[DEBUG] Не выводим {artist_name}, тк он дизлайкнут')


def recommend_by_liked_old(liked_artist_names: str, max_output_len=5):
    liked_artist_names_list = split_artists(liked_artist_names)
    liked_artists = {find_artist(artist.lower()) for artist in liked_artist_names_list}

    artist_recommendations = {}
    for artist in liked_artists:
        artist_recommendations[artist] = get_recommendations(artist, ARTIST_PAIRS_PROXIMITY)

    for liked_artist, rec in artist_recommendations.items():
        print(liked_artist)
        for item, val in rec.items():
            print(item, val)
        print()
        print()

    final_recommendation = {}
    proximity_threshold = 0.6

    for liked_artist1 in liked_artists:
        for liked_artist2 in liked_artists:
            if liked_artist1 == liked_artist2:
                continue
            for recommended_artist_name in artist_recommendations[liked_artist2]:
                recommended_artist = find_artist(recommended_artist_name)
                if liked_artist1 == recommended_artist:
                    continue
                liked_recommended_artists_proximity = generalizing_proximity_measure(
                    TREE, liked_artist1, recommended_artist, max_distance_between_nodes, min_proximity, max_proximity
                )
                if liked_recommended_artists_proximity < proximity_threshold:
                    if recommended_artist in final_recommendation and proximity_threshold < final_recommendation[recommended_artist]:
                        final_recommendation[recommended_artist] = liked_recommended_artists_proximity
                    final_recommendation[recommended_artist] = liked_recommended_artists_proximity
                #print(liked_artist1, recommended_artist, liked_recommended_artists_proximity)

    final_recommendation = sorted(final_recommendation.items(), key=lambda item: item[1])
    for recommended_artist, proximity in final_recommendation:
        print(recommended_artist, proximity)



