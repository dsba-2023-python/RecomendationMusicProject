import random

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
        total = sum(chain[key].values())
        for word in chain[key]:
            chain[key][word] /= total

    sentence = ''
    k = 0
    current_el = 'START'
    k_max = random.randint(7, 15)
    while True:
        all_pairs = chain[current_el]
        current_el = choices(list(all_pairs.keys()), weights=list(all_pairs.values()), k=1)[0]
        if current_el in '!.,)?:\n;\'':
            sentence = sentence.strip()

        if k <= k_max and current_el == 'STOP':
            current_el = 'START'
            continue
        if current_el == 'STOP' and k > k_max:
            break
        sentence += current_el + ' '
        k += 1
        # return chain
    return sentence


def generate_text_v4(text, n_gramms=4) -> list:
    chain = dict()
    tokens = word_tokenize(text)
    change = 0
    for i in range(len(tokens)):
        if tokens[i + change] in {'.', '?', '!', '\n'}:
            tokens.insert(i + 1 + change, 'STOP')
            tokens.insert(i + 2 + change, 'START')
            change += 2
    tokens = ['START'] * (n_gramms - 1) + tokens[:-1]

    for word_ind in range(len(tokens) - (n_gramms - 1)):
        n_g = tuple([tokens[word_ind + i] for i in range(n_gramms - 1)])
        following = chain.get(n_g, dict())
        following[tokens[word_ind + (n_gramms - 1)]] = following.get(tokens[word_ind + (n_gramms - 1)], 0) + 1
        chain.update({n_g: following})

    for key in chain:
        total = sum(chain[key].values())
        for word in chain[key]:
            chain[key][word] /= total
    # print(chain.values())
    print(sum(map(len, chain.values())))

    sentence = ''
    k = 0
    current_el = ['START'] * (n_gramms - 1)
    k_max = random.randint(7, 15)
    while True:
        all_pairs = chain[tuple(current_el)]
        current_el = current_el[1:] + choices(list(all_pairs.keys()), weights=list(all_pairs.values()), k=1)
        if current_el[-1] in '!.,)?:\n;\'':
            sentence = sentence.strip()
        #
        # if k <= k_max and current_el == 'STOP':
        #     current_el = 'START'
        #     continue

        if current_el[-1] == 'STOP':
            break
        sentence += current_el[-1] + ' '
        k += 1
        # return chain
    return sentence


if __name__ == "__main__":
    n_gramms = 4
    data = get_bio()
    print(generate_text_v4(f' STOP {"START " * (n_gramms - 1)}  '.join(data) + '.', n_gramms))
