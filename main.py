from preprocesamiento import preProccesing




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


def l_and(arg1, arg2):
    res = []
    index1 = 0
    index2 = 0

    while index1 < len(arg1) and index2 < len(arg2):
        if(arg1[index1] == arg2[index2]):
            res.append(arg1[index1])
            index1+=1
            index2+=1
        elif (arg1[index1] < arg2[index2]):
            index1+=1
        else:
            index2+=1
    return res

def l_or(arg1, arg2):
    res = []
    index1 = 0
    index2 = 0

    while index1 < len(arg1) or index2 < len(arg2):
        if(index1 < len(arg1) and index2 < len(arg2)):
            if(arg1[index1] == arg2[index2]):
                res.append(arg1[index1])
                index1+=1
                index2+=1
            elif (arg1[index1] < arg2[index2]):
                res.append(arg1[index1])
                index1+=1
            else:
                res.append(arg2[index2])
                index2+=1
        else:
            if(index2 == len(arg2)):
                res.append(arg1[index1])
                index1+=1
            else:
                res.append(arg2[index2])
                index2+=1
    return res


def l_and_not(arg1, arg2):
    res = []
    index1 = 0
    index2 = 0

    while index1 < len(arg1):
        if(arg1[index1] == arg2[index2]):
            index1+=1
            index2+=1
        elif (arg1[index1] < arg2[index2]):
            res.append(arg1[index1])
            index1 += 1
        else:
            index2 += 1
    return res

if __name__ == "__main__":
    i = preProccesing()
    i.creatingFrequency()
    term1 = i.L("Bilbo")
    term2 = i.L("Anillo")



    print(l_and(term1, term2 ) )
    print(l_or(term1, term2 ) )
    print(l_and_not(term2, term1 ) )









