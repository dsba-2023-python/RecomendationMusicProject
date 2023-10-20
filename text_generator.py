from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from lastfm import parse_genius
import re
import pickle
from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    PER,
    NamesExtractor,

    Doc
)

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

names_extractor = NamesExtractor(morph_vocab)


def get_artist(name):
    url = f"https://genius.com/artists/{name}/songs"
    response = requests.get(url).content
    soup = BeautifulSoup(response, "html.parser")
    soup = soup.find_all('h3')
    songs = map(lambda x: re.search("\([a-zA-Z0-9\s]+\)", x.text), soup)
    #print(*songs)
    lyrics = []
    for i in tqdm(songs):
        if not i:
            continue
        res = parse_genius(name, i.group()[1:-1])
        if not res:
            continue
        lyrics.append(res)
    with open('data.pickle', 'wb') as f:
        pickle.dump(lyrics, f, pickle.HIGHEST_PROTOCOL)
def parse_text(text):
    #doc = Doc(text)
    #doc.segment(segmenter)
    #doc.tag_morph(morph_tagger)
    #return doc.tokens
    text = text.split()
    

if __name__ == "__main__":
    # get_artist('Basta')
    with open('data.pickle', 'rb') as f:
        data = pickle.load(f)
    print(parse_text(data[0]))
