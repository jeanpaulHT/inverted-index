from preprocessor import Preprocessor
from index import Index
from queries import Query


def main():
    books = [f"libro{i}.txt" for i in range(1, 7)]
    book_dir = "./texts/books"
    out_dir = "./texts/preprocessing"
    stop_list = "./texts/stoplist.txt"
    index_file = "./texts/index.txt"

    preprocessor = Preprocessor(book_dir, out_dir, stop_list)
    out_files = preprocessor.preprocess(books)

    index = Index(out_files)
    index.dump(index_file)

    query = Query(index, input("Ingrese una query: "))
    print("result: ", query.eval())


if __name__ == "__main__":
    main()

    # term1 = _index.L("Bilbo")
    # term2 = _index.L("Anillo")
    # term3 = _index.L("Montaña")
    #
    # print(term1, term2, term3)
    #
    # print(query_and(term1, term2))
    # print(query_or(term1, term2))
    # print(query_and_not(term3, term1))
    # print(query_and_not(term1, term3))
    # print(query_and(term2, term3))
    # print(query_or(term1, term3))

    # query = Query(_index, "Fangorn or (Bilbo and not Montaña) or (Montaña and not Bilbo)")
