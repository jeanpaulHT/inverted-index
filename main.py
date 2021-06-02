import nltk
from nltk.stem import SnowballStemmer


stemmer = SnowballStemmer('spanish')

def loadUneccesaryChar():
    file = "texts/stoplist.txt"
    f = open(file)
    s = {".", "?", "!", "¿", "<", ">", ",", "º", " ", ":", ";", "«", "»"}


    return s

def loadStopList():
    f = open("texts/stoplist.txt", encoding="ISO-8859-1")
    stopList = set()
    for line in f:
        stopList.add(line[:-1])
    return stopList

def parse(str):
    wordList = str.split(" ")
    res = list()
    uneWords =loadUneccesaryChar()
    for word in wordList:
        for c in word:
            if(c in uneWords):
                word = word.replace(c, "")
        res.append(word)

    return res
def read_documents(book):
    file = "texts/books/libro" + str(book) + ".txt"
    f = open(file, encoding="utf-8")
    out = open("texts/preprocessing/libro" + str(book) + ".txt", "w+", encoding="utf-8")
    stoplist = loadStopList()
    for line in f:
        if line != "\n":
            for word in parse(line):
                if word.lower() not in stoplist:
                    out.write(stemmer.stem(word.lower()) + " ")
    f.close()
    out.close()


if __name__ == "__main__":
    # read_documents(1)
    read_documents(1)
    print("a");
