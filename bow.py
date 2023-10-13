import pandas as pd
from lastfm import parse_bio
from tqdm import tqdm
import pickle
import re
import string
from app import cos_dist, E_dist

def fetch_bio():
    bios = []
    df = pd.read_csv("data/playlist_2010to2022 .csv")
    for name in tqdm(df.artist_name.unique()[:30]):
        bios.append(parse_bio(name, False))
    with open('data.pickle', 'wb') as f:
        pickle.dump(bios, f, pickle.HIGHEST_PROTOCOL)

def get_bio():
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
        return data


def preprocess(row) -> list:
    with open('data/stopwords', 'r') as file:
        stopwords = set(map(str.strip, file.readlines()))
    row = row.lower()
    row = re.sub(f"\W+", " ", row).split()
    row = [i for i in row if i not in stopwords]
    return row


def get_dictionary(data) -> dict:
    words_met = dict()
    idx = 0
    for row in tqdm(data):
        row = preprocess(row)
        for word in row:
            if word not in words_met:
                words_met[word] = idx
                idx += 1
    matrix = []
    for row in data:
        row = preprocess(row)
        vector = [0] * len(words_met)
        for word in row:
            vector[words_met[word]] += 1
        matrix.append(vector)
    return matrix


def compare_bio(matrix):
    for i, vector1 in enumerate(matrix):
        for j, vector2 in enumerate(matrix):
            if i >= j:
                continue
            print(i, j, E_dist(vector1, vector2))




if __name__ == "__main__":
    print(compare_bio(get_dictionary(get_bio())))

