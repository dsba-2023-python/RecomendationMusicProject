import argparse
from typing import List, Tuple
import pandas as pd

TRACK_COLUMN = 3
POPULAR_TRAC_COLUMN = 4
ARTIST_NAME_COLUMN = 7
GENRE_COLUMN = 8
YEAR_COLUMN = 1
SONGE_ID_COLUMN = 2
M = 9


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
    m = dict()
    for i in table:
        m[i[7]] = m.get(i[7], 0) + 1
    return sorted(m.items(), key=lambda x: x[1], reverse=True)[:n]


def top_n_songs_by_artist(table, artist, n):
    table = list(filter(lambda x: artist == x[ARTIST_NAME_COLUMN], table))
    table.sort(key=lambda x: x[POPULAR_TRAC_COLUMN], reverse=True)

    return list(map(lambda x: (x[TRACK_COLUMN], x[POPULAR_TRAC_COLUMN]), table))[:n]


def top_n_songs_by_years(table, year: int, n: int):
    if isinstance(year, tuple):
        year = sorted(year)
        table = list(filter(lambda x: year[0] <= x[YEAR_COLUMN] <= year[-1], table))
    else:
        table = list(filter(lambda x: year == x[YEAR_COLUMN], table))
    table.sort(key=lambda x: x[POPULAR_TRAC_COLUMN], reverse=True)

    return list(map(lambda x: (x[TRACK_COLUMN], x[YEAR_COLUMN], x[ARTIST_NAME_COLUMN], x[POPULAR_TRAC_COLUMN]), table))[
           :n]


def top_n_songs_for_a_genre(table, genre, n):
    def parse_list(stroka):
        return stroka[2:-2].split("', '")

    table = list(filter(lambda x: genre in parse_list(x[GENRE_COLUMN]), table))
    table.sort(key=lambda x: x[POPULAR_TRAC_COLUMN], reverse=True)

    return list(map(lambda x: (x[TRACK_COLUMN], x[ARTIST_NAME_COLUMN], x[POPULAR_TRAC_COLUMN]), table))[:n]


def similar_songs(table, song_id, n):
    smt = []

    def evklid(lst1, lst2):
        lst3 = zip(lst1, lst2)

        return sum([(i[0] - i[1]) ** 2 for i in lst3]) ** (0.5)

    for i in table:
        if song_id == i[SONGE_ID_COLUMN]:
            lst1 = i[M:]
            break
    for i in table:
        if song_id != i[SONGE_ID_COLUMN]:
            lst2 = i[M:]
            smt.append((evklid(lst1, lst2), i))
    return sorted(smt)[:n]


def test(table):
    print(similar_songs(table, "7iXF2W9vKmDoGAhlHdpyIa", 5))
    # print(get_table_shape(table))
    # print(get_column_stat(table, 12, "max"))
    # print(get_top_artist_count(table))


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

    if args.top_artists:
        n = get_top_artist_count(db, args.top_artists)
        for i, p in enumerate(n):
            print(f'{i + 1}) {p[0]}: {p[1]}')

    if args.column_index:
        print(
            f"{args.stats} is {get_column_stat(db, args.column_index, args.stats)} for {args.column_index} column!"
        )

test(db)
