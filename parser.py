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

prefixes = ['u', 'be', 'for', 'over', 'under', 'av', 'inn', 'ut']
suffixes = ['het', 'else', 'skap', 'lighet', 'dom', 'sjon', 'eri']

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


def gen_random_from_list(words, num) -> list:
    new_words = []
    old_words = [word for word in words if len(word) >= 3]
    print("old word list length: ", len(old_words))
    for i in range(num):
        index = random.randrange(0, len(old_words))
        old_word = old_words[i]
        #print("Old word: " + old_word)
        limit = int(len(old_words[index]) / 1.1) + 1

        # create a new word from the first 3 characters in the current word from the word list
        # concatenated with 2-3 characters from another random word (min length 3)
        new_words.append(old_word[:3] + old_words[index][:random.randrange(3,limit)])

    return new_words


def gen_from_adjektiv():
    quit: bool = False
    lines_list = []

    with open(adj_sub_path + adjektiv.name + adjektiv.filetype, 'r', encoding='utf-8') as f:
        for line in f:
            lines_list.append(line.strip().lower())

    new_words = gen_random_from_list(lines_list, 10)

    for word in new_words:
        print(word)

def iterate():
    lines = 0

    # Open a file, and iterate over the words
    # with open (adj_sub_path + adj_sub_files[lines % len(adj_sub_files)], 'r', encodind='utf-8')
    with open(adj_sub_path + adj_sub_files[lines], 'r', encoding='utf-8') as f:
        while lines < 20:
            lines += 1
            line = f.readline()
            print(line)

def generate_word():
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

# Generer og skriv ut 10 nye ord
# for _ in range(10):
#    print(generate_word())

if __name__ == '__main__':
    gen_from_adjektiv()

# vvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# TTTTTTTTTT  ooo   DDD    ooo  
#     TT     O   O  D  D  O   O
#     TT     O   O  D  D  O   O
#     TT      OOO   DDD    OOO 
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# [x] - Adjektiv
# [ ] - Substantiv
# [ ] - Mer

