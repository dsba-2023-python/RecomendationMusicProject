import pandas as pd
from lastfm import get_artist_bio
from tqdm import tqdm
import pickle
from string import digits, punctuation


def bio_artist():
    df = pd.read_csv('data/playlist_2010to2022.csv')
    names = df.artist_name.unique()[:30]
    artist_bio = []
    for name in tqdm(names):
        artist_bio.append(get_artist_bio(name, False))
    with open('data.pickle', 'wb') as f:
        pickle.dump(artist_bio, f, pickle.HIGHEST_PROTOCOL)


def get_bio_artist():
    with open('data.pickle', 'rb') as f:
        return pickle.load(f)

def preprocess_file(data):
    with open('data/stop_words.txt', 'r') as f:
        stop_words = {i.strip() for i in f}
    b = set()
    for i in data:
        for j in digits + punctuation:
            i = i.replace(j, ' ')
        b |= set(i.lower().split()) - stop_words
    # print(len(set(get_bio_artist().split())))
    print(len(b))

if __name__ == '__main__':
    data = get_bio_artist()
    preprocess_file(data)
