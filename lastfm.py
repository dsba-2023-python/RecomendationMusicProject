from bs4 import BeautifulSoup
import requests
import random


def parse_bio_short(soup):
    content = soup.find("div", {"class": "wiki-block-inner-2"})
    if not content:
        return 'Artist does not exist'
    return '\n\n'.join([el.text for el in content.findAll("p")])


def parse_bio_long(soup):

    content = soup.find("div", {"class": "wiki-content"})
    if not content:
        return 'Artist does not exist'
    return '\n\n'.join([el.text for el in content.findAll("p")])


def parse_bio(artist, is_short=True):
    if is_short:
        link = f"https://www.last.fm/music/{artist}"
    else:
        link = f"https://www.last.fm/music/{artist}/+wiki"

    res = requests.get(link).content
    soup = BeautifulSoup(res, "html.parser")
    if is_short:
        return parse_bio_short(soup)
    return parse_bio_long(soup)


def top_n_songs(artist, n=5):
    resp = []
    link = f"https://www.last.fm/music/{artist}/+tracks?date_preset=ALL#top-tracks"
    res = requests.get(link).content
    soup = BeautifulSoup(res, "html.parser")
    content = soup.find("tbody").findAll("tr")
    for song in content[:n]:
        name = song.find("td", {"class": "chartlist-name"}).text.strip()
        number = song.find("span", {"class": "chartlist-count-bar-value"}).text.strip()
        resp.append((name, number))
    return resp

def similar_artists(artist, n=5):
    playlist = []

    link = f"https://www.last.fm/ru/music/{artist}/+similar"
    res = requests.get(link).content
    soup = BeautifulSoup(res, "html.parser")
    content = soup.findAll('h3', {"class": "similar-artists-item-name"})
    names = [el.text.strip() for el in content]

    for art in names:
        top = top_n_songs(art, n=3)
        playlist.extend([(art, song[0]) for song in top])

    random.shuffle(playlist)
    return playlist

def get_lyrics():
    link = "https://genius.com/Dj-khaled-wild-thoughts-lyrics"
    res = requests.get(link).content
    soup = BeautifulSoup(res, "html.parser")
    return soup

if __name__ == "__main__":
    print(get_lyrics())
