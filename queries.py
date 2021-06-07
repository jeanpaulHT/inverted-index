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

    def __init__(self, index: Index, query: str, use_cache: bool = True):
        processed = query.lower()
        processed = processed.replace(" and not ", " - ")
        processed = processed.replace(" and ", " * ")
        processed = processed.replace(" or ", " + ")
        processed = processed.replace("(", " ( ").replace(")", " ) ")
        self._tokens = deque(processed.split())
        self._index = index
        self._use_cache = use_cache
        if use_cache:
            self.cache = dict()

    def eval(self):
        value = self._expression()
        Query._expect(self._current() is None, f"Expected end of query, got {self._current()}")
        return value

    def _expression(self):
        result = self._terminal()
        while self._current() == '+':
            self._advance()
            result = l_or(result, self._terminal())
        return result

    def _terminal(self):
        result = self._value()
        while self._current() in ('*', '-'):
            if self._current() == '*':
                self._advance()
                result = l_and(result, self._terminal())
            if self._current() == '-':
                self._advance()
                result = l_and_not(result, self._terminal())
        return result

    def _value(self):
        Query._expect(self._current() is not None, "Finished parsing without success")
        if self._current().isalpha():
            return self._load(self._consume())

        if self._current() == '(':
            self._advance()
            result = self._expression()
            Query._expect(self._consume() == ")", "Unmatched parenthesis on query")
            return result

        Query._fail(f"Expected a word or a nested query, got {self._current()}")

    def _load(self, word):
        if self._use_cache and word in self.cache:
            return self.cache[word]

        return_value = self._index.L(word)
        if self._use_cache:
            self.cache[word] = return_value

        return return_value

    @staticmethod
    def _expect(boolean_expr, message):
        if not boolean_expr:
            Query._fail(message)

    @staticmethod
    def _fail(message):
        raise ValueError("Parser Error: ", message)

    def _current(self):
        return self._tokens[0] if len(self._tokens) > 0 else None

    def _consume(self):
        tmp = self._current()
        assert tmp is not None
        self._advance()
        return tmp

    def _advance(self):
        self._tokens.popleft()
