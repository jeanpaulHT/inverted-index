from preprocesamiento import preproccesing

def creatingFrequency():
    words = {}
    for book in range(1,7):
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
    result = sorted(filtered, key=lambda item:item[0])
    return result


def writingFreqFile(freqList,file):
    f = open(file, "w+", encoding="utf-8")
    for row in freqList:
        line = str(row[0]) + ":"
        comma = False
        for book in row[1][1]:
            if(comma):
                line += ","
            line += str(book)
            comma = True
        f.write(line+'\n')

if __name__ == "__main__":
    # preproccesing()
    print("creating frequency list....")
    result = creatingFrequency()
    print("frequency done")
    file = "frequency.txt"
    print("creating file for frequency list....")
    writingFreqFile(result,file)







