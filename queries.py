from collections import deque
from index import Index


def l_and(arg1, arg2):
    res = []
    index1 = 0
    index2 = 0

    while index1 < len(arg1) and index2 < len(arg2):
        if arg1[index1] == arg2[index2]:
            res.append(arg1[index1])
            index1 += 1
            index2 += 1
        elif arg1[index1] < arg2[index2]:
            index1 += 1
        else:
            index2 += 1
    return res


def l_or(arg1, arg2):
    res = []
    index1 = 0
    index2 = 0

    while index1 < len(arg1) or index2 < len(arg2):
        if index1 < len(arg1) and index2 < len(arg2):
            if arg1[index1] == arg2[index2]:
                res.append(arg1[index1])
                index1 += 1
                index2 += 1
            elif arg1[index1] < arg2[index2]:
                res.append(arg1[index1])
                index1 += 1
            else:
                res.append(arg2[index2])
                index2 += 1
        else:
            if index2 == len(arg2):
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
        if arg1[index1] == arg2[index2]:
            index1 += 1
            index2 += 1
        elif arg1[index1] < arg2[index2]:
            res.append(arg1[index1])
            index1 += 1
        else:
            index2 += 1
    return res


class Query:

    def __init__(self, index: Index, query: str):
        processed = query.lower()
        processed = processed.replace(" and not ", " - ")
        processed = processed.replace(" and ", " * ")
        processed = processed.replace(" or ", " + ")
        processed = processed.replace("(", " ( ").replace(")", " ) ")
        self.tokens = deque(processed.split())
        self.index = index
        self.cache = dict()

    def L(self, word):
        if word in self.cache:
            return self.cache[word]

        return_value = self.index.L(word)
        self.cache[word] = return_value
        return return_value

    """
    exp ::= term  | exp + term | exp - term
    term ::= factor | factor * term | factor / term
    factor ::= number | ( exp )
    """

    def current(self):
        return self.tokens[0] if len(self.tokens) > 0 else None

    def exp(self):
        result = self.term()
        while self.current() == '+':
            self.next()
            result = l_or(result, self.term())

        return result

    def factor(self):
        result = None

        if self.current() is None:
            raise ValueError()

        if self.current().isalpha():
            result = self.L(self.current())
            self.next()
        elif self.current() == '(':
            self.next()
            result = self.exp()
            self.next()
        return result

    def next(self):
        self.tokens.popleft()
        return self.current()

    def term(self):
        result = self.factor()
        while self.current() in ('*', '-'):
            if self.current() == '*':
                self.next()
                result = l_and(result, self.term())
            if self.current() == '-':
                self.next()
                result = l_and_not(result, self.term())
        return result
