from bow import get_bio
import nltk
import ssl
from random import choices, choice
import re

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context
#
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk import pos_tag



def generate_text_v1(text: list, n_words=20) -> list:
    tokens = word_tokenize(text)
    return ' '.join(choices(tokens, k=n_words))


def generate_text_v2(text: list, n_words=20) -> list:
    tokens = pos_tag(word_tokenize(text))
    nouns = list(set(filter(lambda x: x[1] == 'NN', tokens)))
    verbs = list(set(filter(lambda x: x[1] == 'VB', tokens)))
    other = list(set(filter(lambda x: x[1] != 'VB', tokens)))
    # [('And', 'CC'), ('now', 'RB'), ('for', 'IN'), ('something', 'NN'),
    #  ('completely', 'RB'), ('different', 'JJ')]
    sentence = [choice(nouns), choice(verbs), choice(nouns)] + choices(other, k=(n_words - 3))
    for i in sentence:
        print(i[0], end=' ')
    return


def generate_text_v3(text, n_words=20) -> list:
    chain = dict()
    tokens = word_tokenize(text)
    change = 0
    for i in range(len(tokens)):
        if tokens[i + change] in {'.', '?', '!', '\n'}:
            tokens.insert(i + 1 + change, 'STOP')
            tokens.insert(i + 2 + change, 'START')
            change += 2
    tokens = ['START'] + tokens[:-1]


    for word_ind in range(len(tokens) - 1):
        following = chain.get(tokens[word_ind], dict())
        following[tokens[word_ind + 1]] = following.get(tokens[word_ind + 1], 0) + 1
        chain.update({tokens[word_ind]: following})


    for key in chain:
        total  = sum(chain[key].values())
        for word in chain[key]:
            chain[key][word] /= total
    return chain

if __name__ == "__main__":
    data = get_bio()
    print(generate_text_v3(data[0] + '.'))
