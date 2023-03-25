import os
from collections import defaultdict
from math import log

DIRECTORY = 'Выкачка_очищенная'
COUNT_DOCUMENTS = 100


def count_tf(terms):
    tf_dict = defaultdict(float)
    for term in terms:
        tf_dict[term] += 1
    for k, v in tf_dict.items():
        tf_dict[k] = v / len(terms)
    return tf_dict


def count_idf(terms, terms_in_documents):
    idf_dict = dict()
    for term in terms:
        count_doc_with_term = 0
        for terms_in_document in terms_in_documents:
            if term in terms_in_document:
                count_doc_with_term += 1
        idf_dict[term] = log(COUNT_DOCUMENTS / count_doc_with_term)
    return idf_dict


def count_tf_idf(tf_dict, idf_dict):
    tf_idf_dicts = dict()
    for term, tf_value in tf_dict.items():
        tf_idf_dicts[term] = tf_value * idf_dict[term]
    return tf_idf_dicts


def get_tf_terms(kind):
    terms_overall = []
    terms_in_documents = []
    idx = -1
    tf_documents = [defaultdict(list) for _ in range(COUNT_DOCUMENTS)]
    for root, dirs, files in os.walk(DIRECTORY):
        for file in files:
            if file.lower().endswith('.txt') and file.lower().startswith(kind):
                idx += 1
                path_file = os.path.join(root, file)
                with open(path_file, encoding="utf=8") as f:
                    # if kind == "tokens":
                    terms_in_documents.append(f.read().split('\n'))
                    # else:
                    #     terms_in_documents.append(list(map(lambda x: x.split(':')[0], f.readlines())))
                    tf_documents[idx] = count_tf(terms_in_documents[idx])
                    terms_overall += terms_in_documents[idx]
    terms_overall = list(set(terms_overall))
    idf_terms = count_idf(terms_overall, terms_in_documents)
    tf_idf_dicts = []
    for tf_document in tf_documents:
        tf_idf_terms = count_tf_idf(tf_document, idf_terms)
        tf_idf_dicts.append(tf_idf_terms)
    return tf_idf_dicts, idf_terms


def writing_files(tf_idf_dicts, idf_terms, kind):
    path_result_begin = f"tf_idf_{kind}/tf_idf_{kind}_"
    for i, tf_idf_dict in enumerate(tf_idf_dicts):
        num_file = f'00{i}' if i < 10 else f'0{i}'
        path_result = f'{path_result_begin}{num_file}.txt'
        os.makedirs(os.path.dirname(path_result), exist_ok=True)
        with open(path_result, "w", encoding="utf-8") as file_result:
            for k, v in tf_idf_dict.items():
                file_result.write(k + " " + str(idf_terms[k]) + " " + str(v))
                file_result.write("\n")


if __name__ == '__main__':
    tf_idf_dicts_tokens, idf_tokens = get_tf_terms("tokens")
    writing_files(tf_idf_dicts_tokens, idf_tokens, "tokens")
    tf_idf_dicts_lemmas, idf_lemmas = get_tf_terms("lemmas")
    writing_files(tf_idf_dicts_lemmas, idf_lemmas, "lemmas")
