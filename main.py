from preprocessor import Preprocessor
from queries import QueryEngine


def write_index_to_file(index, file):
    f = open(file, "w+", encoding="utf-8")
    for word, cases in index.items():
        f.write(f"{word}: " + ", ".join(map(str, cases)) + "\n")


def l_and(arg1, arg2):
    res = []
    index1 = 0
    index2 = 0

    while index1 < len(arg1) and index2 < len(arg2):
        if (arg1[index1] == arg2[index2]):
            res.append(arg1[index1])
            index1 += 1
            index2 += 1
        elif (arg1[index1] < arg2[index2]):
            index1 += 1
        else:
            index2 += 1
    return res


def l_or(arg1, arg2):
    res = []
    index1 = 0
    index2 = 0

    while index1 < len(arg1) or index2 < len(arg2):
        if (index1 < len(arg1) and index2 < len(arg2)):
            if (arg1[index1] == arg2[index2]):
                res.append(arg1[index1])
                index1 += 1
                index2 += 1
            elif (arg1[index1] < arg2[index2]):
                res.append(arg1[index1])
                index1 += 1
            else:
                res.append(arg2[index2])
                index2 += 1
        else:
            if (index2 == len(arg2)):
                res.append(arg1[index1])
                index1 += 1
            else:
                res.append(arg2[index2])
                index2 += 1
    return res


def l_and_not(arg1, arg2):
    res = []
    index1 = 0
    index2 = 0

    while index1 < len(arg1):
        if (arg1[index1] == arg2[index2]):
            index1 += 1
            index2 += 1
        elif (arg1[index1] < arg2[index2]):
            res.append(arg1[index1])
            index1 += 1
        else:
            index2 += 1
    return res


if __name__ == "__main__":
    books = [f"libro{i}.txt" for i in range(1, 7)]
    book_dir = "./texts/books"
    out_dir = "./texts/preprocessing"
    stop_list = "./texts/stoplist.txt"
    index_file = "./texts/index.txt"

    preprocessor = Preprocessor(book_dir, out_dir, stop_list)
    out_files = preprocessor.preprocess(books)

    engine = QueryEngine(out_files)

    term1 = engine.L("Bilbo")
    term2 = engine.L("Anillo")

    print(l_and(term1, term2))
    print(l_or(term1, term2))
    print(l_and_not(term2, term1))

    print(engine.inverted_index)
    write_index_to_file(engine.inverted_index, index_file)
