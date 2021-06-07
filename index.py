from nltk.stem import SnowballStemmer


class Index:
    inverted_index = dict()
    _stemmer = SnowballStemmer('spanish')

    def __init__(self, book_paths):
        self.inverted_index = self._make_inverted_index(book_paths)

    def L(self, word):
        return self.inverted_index[Index._stemmer.stem(word.lower())]

    def _make_inverted_index(self, book_names):
        out_words = dict()

        for book_number, book_name in enumerate(book_names, start=1):
            with open(book_name, encoding="utf-8") as file:
                self._accumulate_frequency(book_number, file, out_words)

        freq_table = [(x, y, list(z)) for x, [y, z] in out_words.items()]

        ordered = sorted(freq_table, key=lambda item: -item[1])
        trimmed = ordered[:500]
        filtered = sorted(trimmed, key=lambda item: item[0])

        for x, _, z in filtered:
            self.inverted_index[x] = z

        return self.inverted_index

    @staticmethod
    def _accumulate_frequency(book_index, file, out_words):
        lines = map(lambda x: x.strip(" \n"), file)
        lines = filter(lambda i: len(i) > 0, lines)

        for line in lines:
            if line not in out_words:
                out_words[line] = [1, {book_index}]
            else:
                out_words[line][0] += 1
                out_words[line][1] |= {book_index}
