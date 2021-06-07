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

    def _current(self):
        return self.tokens[0] if len(self.tokens) > 0 else None

    @staticmethod
    def _expect(boolean_expr, message):
        if not boolean_expr:
            Query._fail(message)

    @staticmethod
    def _fail(message):
        raise ValueError("Parser Error: ", message)

    def eval(self):
        value = self._exp()
        Query._expect(self._current() is None, f"Expected end of query, got {self._current()}")
        return value

    def _exp(self):
        result = self._term()
        while self._current() == '+':
            self._advance()
            result = l_or(result, self._term())
        return result

    def _factor(self):
        result = None

        Query._expect(self._current() is not None, "Finished parsing without success")

        if self._current().isalpha():
            result = self.L(self._current())
            self._advance()
        elif self._current() == '(':
            self._advance()
            result = self._exp()
            Query._expect(self._consume() == ")", "Unmatched parenthesis on query")
        else:
            Query._fail(f"Expected a word or a nested query, got {self._current()}")
        return result

    def _advance(self):
        self.tokens.popleft()

    def _consume(self):
        tmp = self.tokens[0]
        self._advance()
        return tmp

    def _term(self):
        result = self._factor()
        while self._current() in ('*', '-'):
            if self._current() == '*':
                self._advance()
                result = l_and(result, self._term())
            if self._current() == '-':
                self._advance()
                result = l_and_not(result, self._term())
        return result
