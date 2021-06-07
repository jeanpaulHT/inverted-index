from nltk.stem import SnowballStemmer

class QueryEngine:
    inverted_index = {}

    def _make_inverted_index(self, book_names):
        words = dict()

        for book_number, book_name in enumerate(book_names, start=1):
            with open(book_name, encoding="utf-8") as file:
                self._count_into_words(book_number, file, words)

        words = {x: [y, list(z)] for x, [y, z] in words.items()}

        sorted_x = sorted(words.items(), key=lambda kv: -kv[1][0])
        filtered = sorted_x[:500]
        filtered = sorted(filtered, key=lambda item: item[0])

        for x, [_, z] in filtered:
            self.inverted_index[x] = z

        return self.inverted_index

    @staticmethod
    def _count_into_words(book_index, file, words):
        lines = map(lambda x: x.strip(" \n"), file)
        lines = filter(lambda i: len(i) > 0, lines)

        for line in lines:
            if line not in words:
                words[line] = [1, {book_index}]
            else:
                words[line][0] += 1
                words[line][1] |= {book_index}

    def L(self, word):
        stemmer = SnowballStemmer('spanish')
        return self.inverted_index[stemmer.stem(word.lower())]

    def __init__(self, book_paths):
        self.inverted_index = self._make_inverted_index(book_paths)
