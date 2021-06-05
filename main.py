from preprocesamiento import preproccesing
from sortedcontainers import SortedSet

def creatingFrequency():
    words = {}
    for book in range(1,7):
        f = open("texts/preprocessing/libro" + str(book) + ".txt")
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
    result = sorted(filtered, key=lambda item:item[0])
    print(result)



if __name__ == "__main__":
    preproccesing()
    print("running main....")
    creatingFrequency()





