import json
import os

from tokenizer import Tokenizer


class Operator:
    AND = "&"
    OR = "|"
    NOT = "!"


PRIORITY = {1: Operator.OR, 2: Operator.AND}

def priority(operator: str) -> int:
    for key, value in PRIORITY.items():
        if value == operator:
            return key
    return -1

operations = {
    Operator.AND: (lambda a, b: a.intersection(b)),
    Operator.OR: (lambda a, b: a.union(b)),
}


class BooleanSearch:

    def __init__(self, inverted_index_path, all_files_indices):
        """
        Конструктор
        @param inverted_index_path: Путь файл с инвертированным индексом
        """
        self.__inverted_index_path = inverted_index_path
        self.__all_files_indices = set(all_files_indices)
        self.__tokenizer = Tokenizer()

        with open(self.__inverted_index_path) as json_file:
            self.__inverted_index = json.load(json_file)

    def search(self, query):
        """
        Производит булев поиск по заданному выражению
        @param query: Выражение
        """
        tokenized_query = self.__tokenize_query(query)
        print("Tokenized query: %s" % " ".join(tokenized_query))

        converted_query = self.__convert_to_polish_notation(tokenized_query)
        result = self.__evaluate(converted_query)
        print(result)

    def __tokenize_query(self, query):
        """
        Лемматизирует слова в заданном выражении
        @param query: Выражение
        @return: Токенизированный список слов
        """
        negations_indices = []
        tokenized_query = []

        for (index, word) in enumerate(query.split(' ')):
            if word == Operator.AND or word == Operator.OR:
                tokenized_query.append(word)
            else:
                if word[0] == Operator.NOT:
                    tokenized_word = self.__tokenizer.clean_text(word[1:])[0]
                    tokenized_query.append(Operator.NOT + tokenized_word)
                else:
                    tokenized_word = self.__tokenizer.clean_text(word)[0]
                    tokenized_query.append(tokenized_word)

        return tokenized_query

    def __get_index(self, word):
        """
        По заданному слову возвращает список индексов документов, которые содержат слово
        Если слово содержит !, то возвращается список, где слово не содержится
        @param word: Слово
        @return: Список индексов документов
        """
        if word[0] == Operator.NOT:
            try:
                indices = set(self.__inverted_index[word[1:0]])
                return self.__all_files_indices.difference_update(indices)
            except KeyError:
                return set()
        else:
            try:
                index = self.__inverted_index[word]
                return set(index)
            except KeyError:
                return set()

    @staticmethod
    def __convert_to_polish_notation(expr):
        result = []
        stack = []
        for element in expr:
            if element not in [Operator.OR, Operator.AND]:
                result.append(element)
            else:
                last = None if not stack else stack[-1]
                while priority(last) >= priority(element):
                    result.append(stack.pop())
                    last = None if not stack else stack[-1]
                stack.append(element)
        for e in reversed(stack):
            result.append(e)
        return result

    def __evaluate(self, tokens):
        """
        На основе выражение в RPN вычисляет булево выражение
        @param expression: RPN выражение
        @return:
        """
        stack = []

        for token in tokens:
            if token in operations:
                arg2, arg1 = stack.pop(), stack.pop()
                result = operations[token](arg1, arg2)
                stack.append(result)
            else:
                stack.append(self.__get_index(token))

        return stack.pop()