from bs4 import BeautifulSoup
import requests
import random
import re


def parse_bio_short(soup):
    content = soup.find("div", {"class": "wiki-block-inner-2"})
    if not content:
        return "Artist does not exist"
    return content.text.strip()


def parse_bio_long(soup):
    content = soup.find("div", {"class": "wiki-content"})
    if not content:
        return "Artist does not exist"
    return "\n\n".join([el.text for el in content.findAll("p")])


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


def parse_tags(artist):
    # tags = []
    link = f"https://www.last.fm/music/{artist}/+tags"
    res = requests.get(link).content
    soup = BeautifulSoup(res, "html.parser")
    tags = [
        i.text.strip() for i in soup.find_all("h3", {"class": "big-tags-item-name"})
    ]

    return tags


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


def parse_photo(artist):
    link = f"https://www.last.fm/ru/music/{artist}/+wiki"
    res = requests.get(link).content
    soup = BeautifulSoup(res, "html.parser")
    return soup.find("div", {"class": "header-new-background-image"})["content"]


def similar_artists(artist, n=10):
    playlist = []

    link = f"https://www.last.fm/music/{artist}/+similar"
    res = requests.get(link).content
    soup = BeautifulSoup(res, "html.parser")
    content = soup.findAll("h3", {"class": "similar-artists-item-name"})
    names = [el.text.strip() for el in content]

    return names
    #
    # for art in names:
    #     top = top_n_songs(art, n=3)
    #     playlist.extend([(art, song[0]) for song in top])
    #
    # random.shuffle(playlist)
    # return playlist


def get_lyrics(artist, song_name):
    result = []

    if artist.count(" ") > 0:
        artist = artist.split(" ")
        artist[0] = artist[0].capitalize()
        artist_name = "-".join(artist)
    else:
        artist_name = artist.capitalize()

    if song_name.count(" ") > 0:
        song_name = song_name.split(" ")
        song_title = "-".join(song_name)
    else:
        song_title = song_name

    # pattern = "\"Lyrics__Container-\S*\s\""

    link = f"https://genius.com/{artist_name}-{song_title}-lyrics"
    res = str(requests.get(link).content).replace("<br/>", "\n")
    soup = BeautifulSoup(res, "html.parser")
    parts = soup.findAll("div", {"class": "Lyrics__Container-sc-1ynbvzw-1"})
    # parts = soup.findAll("div", {"class": re.match(pattern, res)})

    for part in parts:
        strings = part.text.split("\n")
        for string in strings:
            if string != "":
                result.append(string)

    final_text = "\n".join(result)

    return final_text.replace("\\xe2\\x80\\x85", " ").replace("\\xe2\\x80\\x94", " ")


if __name__ == "__main__":
    print(parse_photo("Drake"))
    # print(get_lyrics("the weeknd", "heartless"))
