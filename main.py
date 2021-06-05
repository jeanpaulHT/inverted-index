from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer('spanish')


def loadUneccesaryElemts():
    s = {".", "?", "!", "¿", "<", ">", ",", "º", " ", ":", ";", "«", "»"}

    return s


def loadStopList():
    f = open("texts/stoplist.txt", encoding="ISO-8859-1")
    stopList = set()
    for line in f:
        # when reading it gives a \n char, we ignored it
        stopList.add(line[:-1]) 
    return stopList


def parse(str):
    wordList = str.split(" ")
    res = list()
    unusedElem = loadUneccesaryElemts()
    for word in wordList:
        for c in word:
            if (c in unusedElem):
                word = word.replace(c, "")
        res.append(word)

    return res


def read_documents(book):
    file = "texts/books/libro" + str(book) + ".txt"
    f = open(file, encoding="utf-8")
    out = open("texts/preprocessing/libro" + str(book) + ".txt", "w+", encoding="utf-8")
    stoplist = loadStopList()
    for line in f:
        if line != "\n" and line != " ":
            for word in parse(line):
                if word.lower() not in stoplist:
                    out.write(stemmer.stem(word.lower()) + "\n")
    f.close()
    out.close()


if __name__ == "__main__":
    for i in range(1, 7):
        print("done " + str(i))
        read_documents(i)
