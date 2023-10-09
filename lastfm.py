import requests
from bs4 import BeautifulSoup


def short_text(soup):
    short_wiki = soup.find("div", {"class": "wiki-block-inner-2"})
    if not short_wiki:
        return "Artist does not exist"
    return short_wiki.text


def long_text(soup):
    long_wiki_div = soup.find("div", {"class": "wiki-content"})
    if not long_wiki_div:
        return "Artist does not exist"
    long_wiki = long_wiki_div.find_all("p")
    return "\n".join([p.text for p in long_wiki])


def parsing_article(artist: str, is_short=True):
    if not is_short:
        link = f"http://www.last.fm/music/{artist}/+wiki"
    else:
        link = f"http://www.last.fm/music/{artist}"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    if not is_short:
        return long_text(soup)
    return short_text(soup)


def parsing_top_tracks(artist: str, n=5):
    link = f"https://www.last.fm/music/{artist}/+tracks?date_preset=ALL#top-tracks"
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    top_songs = soup.find("table", {"class": "chartlist"}).find_all("tr", {"class": "chartlist-row"})
    top_n_track = [(i.find("td", {"class": "chartlist-name"}).text.strip(), i.find("span", {"class": "chartlist-count-bar-value"}).text.strip()) for i in top_songs[:n]]

    print(top_n_track)


if __name__ == "__main__":
    # x = parsing_article("ewqrewefg21124bzk1x4bz21r")
    x = parsing_top_tracks("Drake")
