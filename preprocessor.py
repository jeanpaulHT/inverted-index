from nltk.stem import SnowballStemmer


def load_stop_list(stop_list_path):
    stop_list = set()
    with open(stop_list_path, encoding="ISO-8859-1") as file:
        for line in file:
            stripped = line.strip(" \n")
            if len(stripped) == 0:
                continue
            stop_list.add(stripped)
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

    def __init__(self, in_dir, out_dir, stop_list_path):
        self.stop_list = load_stop_list(stop_list_path)
        self.in_dir = f"./{in_dir}/"
        self.out_dir = f"./{out_dir}/"

    def preprocess_file(self, file, out_name):
        stemmer = SnowballStemmer('spanish')

        with open(file, encoding="utf-8") as f, open(out_name, "w+", encoding="utf-8") as out:
            for line in f:
                if line == "\n" and line == " ":
                    continue
                for word in parse_line(line, self.skipped_symbols):
                    if word not in self.stop_list and not word.isnumeric():
                        out.write(stemmer.stem(word) + "\n")

    def preprocess(self, files):
        out_files = []
        for file in files:
            book, out = self.in_dir + file, self.out_dir + file
            out_files.append(out)
            self.preprocess_file(book, out)
            print("document " + file + " preproccesing done")

        return out_files
