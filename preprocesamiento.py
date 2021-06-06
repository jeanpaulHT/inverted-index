from nltk.stem import SnowballStemmer


def load_stop_list(stop_list_path):
    stop_list = set()
    with open(stop_list_path, encoding="ISO-8859-1") as f:
        for line in f:
            stop_list.add(line[:-1])
    return stop_list


def parse_line(line, skipped):
    word_list = line.split(" ")
    res = list()
    for word in word_list:
        new_word = ""
        for c in word:
            if c not in skipped:
                new_word += c.lower()
        if len(new_word) != 0:
            res.append(new_word)
    return res


class Preprocessor:
    skipped_symbols = {".", "?", "!", "¿", "<", ">", ",", "º", " ", ":", ";", "«", "»", "(", ")", "\n", "\0"}
    invertedIndex = {}

    def __init__(self):
        self.stop_list = load_stop_list("texts/stoplist.txt")
        pass

    def preprocess_documents(self, file, out_name):
        stemmer = SnowballStemmer('spanish')

        with open(file, encoding="utf-8") as f, open(out_name, "w+", encoding="utf-8") as out:
            for line in f:
                if line == "\n" and line == " ":
                    continue
                for word in parse_line(line, self.skipped_symbols):
                    if word not in self.stop_list and not word.isnumeric():
                        out.write(stemmer.stem(word) + "\n")

    def preprocess(self):
        for i in range(1, 7):
            book = f"texts/books/libro{i}.txt"
            out_name = f"texts/preprocessing/libro{i}.txt"
            self.preprocess_documents(book, out_name)
            print("document " + str(i) + " preproccesing done")

    def create_frequency_table(self, book_names=None):
        if book_names is None:
            book_names = [f"texts/preprocessing/libro{book}.txt" for book in range(1, 7)]

        words = dict()
        for book, book_name in enumerate(book_names, start=1):
            with open(book_name, encoding="utf-8") as file_handle:
                for line in file_handle:
                    if line == " " or line == "\n":
                        continue
                    line = line[:-1]
                    if line in words:
                        words[line][0] = words[line][0] + 1
                        if book not in words[line][1]:
                            words[line][1].append(book)
                    else:
                        words[line] = [1, [book]]
        sorted_x = sorted(words.items(), key=lambda kv: -kv[1][0])
        filtered = sorted_x[:500]
        filtered = sorted(filtered, key=lambda item: item[0])

        for x, [_, z] in filtered[0:len(filtered) - 1]:
            self.invertedIndex[x] = z

        return self.invertedIndex

    def L(self, word):
        stemmer = SnowballStemmer('spanish')
        return self.invertedIndex[stemmer.stem(word.lower())]
