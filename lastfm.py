import requests
from bs4 import BeautifulSoup
import random


def parse_full_bio(soup):
    bio = soup.find("div", {"class": "wiki-content"})

    if not bio:
        return "Artist does not exist or there is no bio!"

    return "\n".join([p.text for p in bio.find_all("p")])


def parse_short_bio(soup):
    bio = soup.find("div", {"class": "wiki-block-inner-2"})
    if not bio:
        return "Artist does not exist or there is no bio!"

    return bio.text.strip()


def get_artist_bio(artist: str, is_short=True):
    if is_short:
        link = f"https://www.last.fm/music/{artist}"
    else:
        link = f"https://www.last.fm/music/{artist}/+wiki"

    response = requests.get(link)
    if response.status_code != 200:
        return "Artist does not exist!"

    soup = BeautifulSoup(response.content, "html.parser")

    if is_short:
        return parse_short_bio(soup)

    return parse_full_bio(soup)


def get_top_n_songs(artist, n=5):
    n_songs = []
    link = f"https://www.last.fm/music/{artist}/+tracks?date_preset=ALL#top-tracks"
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")

    chartlist = soup.find("table", {"class": "chartlist"})
    songs = chartlist.find_all("tr", {"class": "chartlist-row"})
    for song in songs[:n]:
        song = song.find("td", {"class": "chartlist-name"})
        n_songs.append((song.text.strip(), song.a["href"]))


    return n_songs


def create_similar_playlist(artist):
    playlist = []
    link = f"https://www.last.fm/music/{artist}/+similar"
    response = requests.get(link)
    soup = BeautifulSoup(response.content, "html.parser")

    artists = soup.find_all("h3", {"class": "similar-artists-item-name"})
    for a in artists:
        top_by_artist = get_top_n_songs(a.text.strip(), 3)
        # playlist.append((a.text.strip(), top_by_artist[0], f"https://www.last.fm{top_by_artist[1]}"))

    random.shuffle(playlist)

    return playlist

if __name__ == "__main__":
    print(create_similar_playlist("Drake"))
