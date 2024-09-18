#!/usr/bin/env python3
#
#
# Oppbygningen av Ordbanken:
#
# Lemmaer:              Grunnformene av ord med tilhørende informasjon.
# Paradigmer:           Bøyningsmønstre som viser hvordan lemmaer bøyes.
# Koblinger:            Filer som kobler lemmaer til deres paradigmer og bøyningsformer.
# Morfologisk analyse:  Dybdeinformasjon om ords struktur og bøyning.
# Argumentstrukturer:   Spesielt for verb, gir innsikt i syntaktiske mønstre.
#
# (ℹ)
# Dette er en passfrasegenerator, med en tvist.
# Generatoren genererer ikke-eksisterende 'norske' ord 
# for bruk senere i f.eks. passfrasegenerasjon
# 
# EKSEMPLER
#  - yrthes
#  - ørtspråk
#  - penfluvia
#  - garkampkla
#  - renbry
#  - rakartsri
#  - purkuleru
#  - barslesk
#  - penfla
#  - renglu
#  - bartobeint
#  - rakpen
# 
#################################################################################
import os.path
import random
from collections import defaultdict

prefixes = ['u', 'be', 'for', 'over', 'under', 'av', 'inn', 'ut', 'om', 'vel', 'fabel']
suffixes = ['het', 'else', 'skap', 'lighet', 'dom', 'sjon', 'eri', 'art', 'het', 'vet', 'ilt', 'aktig', 'an', 'ig', 'som']

path = 'data/ordbank/'
dir = os.path.dirname(path)

class wordfiles:
    name:       str # the name of the file
    lines:      int # lines in the file (check with wc -l <file>)
    filetype:   str # file type (.txt, .csv, ...)
    
    def __init__(self, name, lines, type):
        self.name = name
        self.lines = lines
        self.filetype = type

adjektiv = wordfiles('adjektiv', 406, '.txt')
substantiv = wordfiles('substantiv', 4421, '.txt')

# Adjektiv, substantiv 
adj_sub_path = 'data/'
adj_sub_files = [adjektiv, 'adjektiv_bestemt', 'adjektiv_bestemt2', 'substantiv']
argparams = ['boying_grupper', 'boying', 'fullformsliste', 'leddanalyse', 'lemma'];
file_type = '.txt'

# gen_passphrase(): generates a passphrase of n @count words from @words list.
# @words<list()>  : list of words to generate phrase from
# @count<int>     : amount of words in phrase
# @separator<char>: character to use as word separator
# @returns        : a string with the passphrase
def gen_passphrase(words: list(), count, separator) -> str:
    passphrase = ""
    for i in range(count):
        index = random.randrange(0, len(words)) # random word from the list
        passphrase += words[index] + separator
    return passphrase[:len(passphrase)-1]       # remove the trailing separator

def gen_random_from_list(words, num) -> list:
    new_words = []
    old_words = [word for word in words if len(word) >= 3] # Remove words with <3 characters 
    random.shuffle(old_words)
    num = len(old_words) if num > len(old_words) else num  # Mitigate out of bounds error
    for i in range(num):
        index = random.randrange(0, len(old_words))
        old_word = old_words[i]
        limit = int(len(old_words[index]))

        # Create a new word from the first 3 characters in the current word from the word list
        # Concatenated with 2-3 characters from another random word (min length 3)
        new_words.append(old_word[:3] + old_words[index][random.randrange(2,limit):])

    return new_words


# gen_from_adjektiv(): Generates a list of @count random words
# @count<int>        : Amount of words to generate
# @count<wordfile>   : Which wordfile to use
# returns a list of random words 
def gen_from_adjektiv(count: int, wf: wordfiles) -> list:
    quit: bool = False
    lines_list = []

    with open(adj_sub_path + wf.name + wf.filetype, 'r', encoding='utf-8') as f:
        for line in f:
            lines_list.append(line.strip().lower())

    random.shuffle(lines_list)
    new_words = gen_random_from_list(lines_list, count)

    for word in new_words:
        print(word)

    return new_words

def generate_word():
    with open(adj_sub_path + adjektiv.name + adjektiv.filetype, 'r', encoding='utf-8') as f:
        lemmas = [line.strip().lower() for line in f]

    root = random.choice(lemmas)
    use_prefix = random.choice([True, False])
    use_suffix = random.choice([True, False])
    
    # Sørg for at minst ett affiks brukes
    if not use_prefix and not use_suffix:
        return generate_word()
    
    word = root
    if use_prefix:
        prefix = random.choice(prefixes)
        word = prefix + word
    if use_suffix:
        suffix = random.choice(suffixes)
        word = word + suffix
    # Sjekk om ordet allerede eksisterer
    if word in lemmas:
        return generate_word()
    return word

# build_markov_model(): https://en.wikipedia.org/wiki/Markov_model
# (i) builds a markov model based off of common word sequences
# @words              : words to build with
def build_markov_model(words):
    model = defaultdict(list)
    for word in words:
        word = f'^{word}$'
        for i in range(len(word) - 2):
            key = word[i:i+2]
            model[key].append(word[i+2])
    return model

def generate_word_markov(model):
    # find all alle keys starting with '^'
    start_keys = [k for k in model.keys() if k.startswith('^')]
    if not start_keys:
        return ''

    current = random.choice(start_keys) # choose random key
    result = current[1:]
    while True:
        key = current[-2:]
        next_chars = model.get(key, None)
        if not next_chars:
            break
        next_char = random.choice(next_chars)
        if next_char == '$':
            break
        result += next_char
        current += next_char
    return result

def read_words(wf: wordfiles) -> list:
    lines_list = []

    with open(adj_sub_path + wf.name + wf.filetype, 'r', encoding='utf-8') as f:
        for line in f:
            lines_list.append(line.strip().lower())
    return lines_list

if __name__ == '__main__':
    word_list = read_words(adjektiv) + read_words(substantiv)
    words = gen_from_adjektiv(10, adjektiv) + gen_from_adjektiv(10, substantiv)

    print(f"Building markov model based off of {len(word_list)} words")
    markov_model = build_markov_model(word_list)
    for _ in range(10):
        word = generate_word()
        #print(word)
        words.append(word)
        print("markov_model result: ", generate_word_markov(markov_model))

    print("------------------------")
    print("passphrase: ", gen_passphrase(words, 4, ':'))

######################################################
# EXAMPLE WORDS
# --------------------
# yrtblid
# ørtkon
# odtkars
# pensmul
# garvrie
# rendyp
# rakhul
# purjam
# rargråbrun
# barbleik
# inndyrteri
# knallgodtsjon
# behoppklart
# rødhvittsjon
# overferskteri
# uhalvvarmt
# besidt
# utunøytraltsjon
# utfalsktskap
# ufrelsteri
#
# ========================================
# OUTPUT
# -------------
# ❯ ./parser.py
# idetemørkt
# ukomodalt
# spebreit
# bart
# reingt
# flont
# glugt
# mett
# støågult
# katt
# emaisme
# kiase
# lyte
# tove
# garue
# skle
# kysete
# maiage
# trise
# hyrme
# Building markov model based off of 4827 words
# markov_model result:  mone
# markov_model result:  ekke
# markov_model result:  grattelle
# markov_model result:  flyte
# markov_model result:  aue
# markov_model result:  miaskriske
# markov_model result:  ære
# markov_model result:  orde
# markov_model result:  nitte
# markov_model result:  mondt
# ------------------------
# passphrase:  katt:underdermalt:emaisme:velvredt
#
######################################################