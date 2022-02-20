import os.path



path = 'data/ordbank/'
dir = os.path.dirname(path)

fileNames = ['boying_grupper.txt', 'boying.txt', 'fullformsliste.txt', 'leddanalyse.txt'];

lines = 0
with open(path + fileNames[2]) as f:
    while lines < 20:
        lines += 1
        line = f.readline()
        print(line)
