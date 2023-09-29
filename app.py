import argparse
from typing import List, Tuple
import csv
import pandas as pd
from typing import Literal, get_args


ARTIST_CL = 7
TRACK_POPULARITY_CL = 4
TRACK_NAME_CL = 3
GENRES_CL = 8
YEAR_CL = 1
TRACK_CHARACTERISTIC_CLS = (10, 21)
URL_CL = 0

_DISTS = Literal["E_dist", "cos_dist", "E_dist_w_L1"]


def get_table_shape(table: List[List[object]]) -> Tuple[int, int]:
    return len(table) if table else 0, len(table[0]) if len(table) else 0


def get_column_stat(table: List[List[object]], index: int, how: str = "min") -> object:
    if not table:
        return None

    if type(table[0][index]) == list:
        return None

    if how == "min" or how == "max":
        import operator

        comp = operator.gt if how == "max" else operator.lt

        current_value = table[0][index]
        for line in table:
            if comp(line[index], current_value):
                current_value = line[index]

        return current_value


def preprocess_file(file_path: str) -> List[List[object]]:
    df = pd.read_csv(file_path)
    #  TODO: don't use pandas

    return df.values.tolist()


def get_top_artist_count(table, n=5):
    artists = dict()

    for row in table:
        artists[row[ARTIST_CL]] = artists.get(row[ARTIST_CL], 0) + 1


    return sorted(artists.items(), key=lambda x: x[1], reverse=True)[:n]

def get_top_songs_by_artist(table, artist, n=5):
    artist_songs = []

    for row in table:
        if row[ARTIST_CL] == artist:
            artist_songs.append((row[TRACK_NAME_CL], row[TRACK_POPULARITY_CL]))
    
    return sorted(artist_songs, key=lambda x: x[1], reverse=True)[:n]

def get_top_songs_by_genre(table, genre, n=5):
    songs_by_genres = []

    for row in table:
        genres = row[GENRES_CL][1:-1].replace("'", "").split(", ")
        if genre in genres:
            songs_by_genres.append({"artist_name": row[ARTIST_CL], "track_name": row[TRACK_NAME_CL], "track_popularity": row[TRACK_POPULARITY_CL]})

    return sorted(songs_by_genres, key=lambda x: x["track_popularity"], reverse=True)[:n] 

def get_top_songs_by_period(table, period: Tuple[int, int], n=5):
    songs_by_period = []

    for row in table:
        if period[0] <= row[YEAR_CL] <= period[1]:
            songs_by_period.append({"artist_name": row[ARTIST_CL], "track_name": row[TRACK_NAME_CL], "track_popularity": row[TRACK_POPULARITY_CL]})

    return sorted(songs_by_period, key=lambda x: x["track_popularity"], reverse=True)[:n] 

def l1_normalize(v):
    norm = sum([i**2 for i in v]) ** .5
    return [i / norm for i in v]

def E_dist(v1, v2):
    res = 0
    for i in range(len(v1)):
        res += (v1[i] - v2[i]) ** 2
    return res ** .5

def E_dist_w_L1(v1, v2):
    res = 0
    v1 = l1_normalize(v1)
    v2 = l1_normalize(v2)
    for i in range(len(v1)):
        res += (v1[i] - v2[i]) ** 2
    return res ** .5

def cos_dist(v1, v2):
    s1 = sum([v1[i] * v2[i] for i in range(len(v1))])
    s2 = sum([v1[i] ** 2 for i in range(len(v1))])
    s3 = sum([v2[i] ** 2 for i in range(len(v1))])
    cos_similarity = s1 / (s2 * s3) * .5
    cos_distance = 1 - cos_similarity
    return cos_distance


optional_functions = {"E_dist": E_dist, "cos_dist": cos_dist, "E_dist_w_L1": E_dist_w_L1}


def get_top_similar_songs(table, url, func: _DISTS = "E_dist", n=5):
    """
    compare only E-dist
    """
    options = get_args(_DISTS)
    assert func in options, f"'{func}' is not in {options}"

    func = optional_functions[func]
    base_song = []
    base_song_idx = -1
    similar_songs = []

    for idx, row in enumerate(table):
        if row[URL_CL] == url:
            base_song = row
            base_song_idx = idx
            break

    for idx, row in enumerate(table):
        if idx == base_song_idx:
            continue
        dist = func(base_song[TRACK_CHARACTERISTIC_CLS[0]:TRACK_CHARACTERISTIC_CLS[1]], row[TRACK_CHARACTERISTIC_CLS[0]:TRACK_CHARACTERISTIC_CLS[1]])
        similar_songs.append({"artist_name": row[ARTIST_CL], "track_name": row[TRACK_NAME_CL], "dist": dist})


    return sorted(similar_songs, key=lambda x: x["dist"])[:n] 

def test(table):
    # print(get_table_shape(table))
    # print(get_column_stat(table, 12, "max"))
    # print(get_top_artist_count(table))
    print(get_top_similar_songs(table, "https://open.spotify.com/playlist/2fmTTbBkXi8pewbUvG3CeZ", func="E_dist",n=3))
    print(get_top_similar_songs(table, "https://open.spotify.com/playlist/2fmTTbBkXi8pewbUvG3CeZ", func="cos_dist",n=3))
    print(get_top_similar_songs(table, "https://open.spotify.com/playlist/2fmTTbBkXi8pewbUvG3CeZ", func="aboba",n=3))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Music Recommendation Application")
    parser.add_argument("file_path", type=str, help="Input file path for table")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show more info or steps"
    )
    parser.add_argument("-s", "--shape", action="store_true", help="Get database shape")
    parser.add_argument("-i", "--column_index", type=int, help="Column index for stats")
    parser.add_argument("-a", "--stats", type=str, choices=["min", "max", "std"])
    parser.add_argument("-t", "--top_artists", type=int)
    # running not in console
    args = parser.parse_args(["./data/playlist_2010to2022.csv"])

    # running in console
    # args = parser.parse_args()

    if args.verbose:
        print(args)
        print(f"File path: {args.file_path}")

    db = preprocess_file(args.file_path)

    if args.shape:
        shape = get_table_shape(db)
        print(f"Database shape: {shape[0]} rows, {shape[1]} columns")

    if args.column_index:
        print(
            f"{args.stats} is {get_column_stat(db, args.column_index, args.stats)} for {args.column_index} column!"
        )

    if args.top_artists:
        res = get_top_artist_count(db, args.top_artists)
        for idx, el in enumerate(res):
            print(f"{idx + 1}) {el[0]}: {el[1]}")

    test(db)
