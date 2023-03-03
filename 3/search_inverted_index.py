import re
from nltk import RegexpTokenizer
from pymorphy2 import MorphAnalyzer

ALL_DOCUMENTS = set(range(100))


def tokenize(s):
    # токенизатор на регулярных выражениях
    tknzr = RegexpTokenizer(r'[А-Яа-яёЁ(AND)(OR)(NOT)\)\)]+')
    clean_words = tknzr.tokenize(s)
    print(clean_words)
    clean_words = [w.lower() for w in clean_words if w != '']
    return list(clean_words)


def lemmatize(tokens):
    pymorphy2_analyzer = MorphAnalyzer()
    lemmas = []
    for token in tokens:
        if re.match(r'[А-Яа-яёЁ]', token):
            lemma = pymorphy2_analyzer.parse(token)[0].normal_form
            lemmas.append(lemma)
        else:
            lemmas.append(token)
    return lemmas


def priority(oper):
    if oper == 'and':
        return 2
    elif oper == 'or':
        return 1
    return -1


def get_notaion(operands):
    result = []
    stack = []
    for operand in operands:
        if operand not in ['and', 'or']:
            result.append(operand)
        else:
            last = None if len(stack) == 0 else stack[-1]
            while priority(last) >= priority(operand):
                result.append(stack.pop())
                last = None if not stack else stack[-1]
            stack.append(operand)
    for el in reversed(stack):
        result.append(el)
    return result


def get_index(self, word):
    if word[0] == 'not':
        try:
            indices = set(inverted_index[word[1:]])
            return ALL_DOCUMENTS - indices
        except KeyError:
            return set()
    else:
        try:
            index = self.__inverted_index[word]
            return set(index)
        except KeyError:
            return set()


def evaluate(tokens):
    stack = []
    for token in tokens:
        if token in ['and', 'or']:
            arg2, arg1 = stack.pop(), stack.pop()
            if token == 'and':
                result = arg1 | arg2
            else:
                result = arg1 & arg2
            stack.append(result)
        else:
            stack.append(get_index(token))
    return stack.pop()


def search(query):
    operands = lemmatize(tokenize(query))


if __name__ == '__main__':
    # query = input()
    search("( пока ) AND ( привет )")
