from nltk.stem import SnowballStemmer

class preProccesing:
    name = ""
    s = {".", "?", "!", "¿", "<", ">", ",", "º", " ", ":", ";", "«", "»", "(", ")"}
    invertedIndex = {}

    def __init__(self):
        self.name = ""


    def loadStopList(self):
        f = open("texts/stoplist.txt", encoding="ISO-8859-1")
        stopList = set()
        for line in f:
            # when reading it gives a \n char, we ignored it
            stopList.add(line[:-1])
        return stopList

    def parseLine(self,str):
        wordList = str.split(" ")
        res = list()
        unusedElem = self.s
        for word in wordList:
            for c in word:
                if (c in unusedElem):
                    word = word.replace(c, "")
            res.append(word)

        return res

    def preprocess_documents(self,book):
        file = "texts/books/libro" + str(book) + ".txt"
        f = open(file, encoding="utf-8")
        out = open("texts/preprocessing/libro" + str(book) + ".txt", "w+", encoding="utf-8")
        stemmer = SnowballStemmer('spanish')
        stoplist = self.loadStopList()
        for line in f:
            if line != "\n" and line != " ":
                for word in self.parseLine(line):
                    if word.lower() not in stoplist and not word.isnumeric():
                        out.write(stemmer.stem(word.lower()) + "\n")
        f.close()
        out.close()

    def preproccesing(self):
        for i in range(1, 7):
            self.preprocess_documents(i)
            print("document " + str(i) + " preproccesing done")

    def creatingFrequency(self):
        words = {}
        for book in range(1, 7):
            f = open("texts/preprocessing/libro" + str(book) + ".txt", encoding="utf-8")
            for word in f:
                if word != " " and word != "\n":
                    word = word[:-1]
                    if word in words:
                        words[word][0] = words[word][0] + 1
                        if book not in words[word][1]:
                            words[word][1].append(book)
                    else:
                        words[word] = [1, [book]]
        sorted_x = sorted(words.items(), key=lambda kv: -kv[1][0])
        filtered = sorted_x[:500]
        filtered = sorted(filtered, key=lambda item: item[0])

        for x, [y,z] in filtered[0:len(filtered) - 1]:
            self.invertedIndex[x] = z

        return self.invertedIndex

    def L(self,word):
        stemmer = SnowballStemmer('spanish')
        # print(stemmer.stem(word.lower()))
        return self.invertedIndex[stemmer.stem(word.lower())]
