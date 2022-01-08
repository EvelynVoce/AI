from csv import reader
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from math import log
from numpy import argmax


class QNAPair:
    def __init__(self, row):
        self.question: str = row[0]
        self.answer: str = row[1]


def reading_csv() -> list[QNAPair]:
    with open("knowledge.csv") as csv_file:
        csv_reader = reader(csv_file, delimiter=',')
        next(csv_reader)  # Skip the first line because it's just the headings for the columns
        return [QNAPair(row) for row in csv_reader]


def get_term_freq(word_dict: dict, bag_of_words: dict[str]) -> dict:
    return {word:  (count / float(len(bag_of_words))) for (word, count) in word_dict.items()}


def get_num_of_words(bag_of_words_test: dict[str], unique_words: set[str]) -> dict:
    bag_of_words_test_lower: set[str] = {word.lower() for word in bag_of_words_test}
    num_of_words_test: dict = dict.fromkeys(unique_words, 0)
    for word in bag_of_words_test_lower:
        num_of_words_test[word] += 1
    return num_of_words_test


def get_all_term_freq(documents, unique_words) -> list[dict]:
    num_of_words: list[dict] = [get_num_of_words(document.split(), unique_words) for document in documents]
    return [get_term_freq(num_of_words[index], document.split()) for index, document in enumerate(documents)]


def get_idf(documents: list[dict]) -> dict:
    idf_dict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, frequency in document.items():
            if frequency > 0:
                idf_dict[word] += 1

    amount_of_docs: int = len(documents)
    for word, val in idf_dict.items():
        idf_dict[word]: float = log(amount_of_docs / val)
    return idf_dict


def get_tfidf(tf_bag_of_words: dict, idfs: dict) -> dict:
    return {word: (val * idfs[word]) for word, val in tf_bag_of_words.items()}


def get_similar(user_input: str) -> str:
    qna_list: list[QNAPair] = reading_csv()
    docs: list[str] = [q.question for q in qna_list]
    docs.append(user_input)  # Add the user input as the final document

    unique_words: set[str] = {word.lower() for document in docs for word in document.split()}
    tfs: list[dict] = get_all_term_freq(docs, unique_words)
    idfs: dict = get_idf([get_num_of_words(document.split(), unique_words) for document in docs])
    tfidfs: list[dict] = [get_tfidf(tf, idfs) for tf in tfs]
    return calc_cos_similarity(pd.DataFrame(tfidfs), qna_list)


def calc_cos_similarity(df, qna_list: list[str]) -> str:
    cosine_similarity_scores: list[list[int]] = cosine_similarity(df.iloc[:-1], df.iloc[-1:])
    max_index = argmax(cosine_similarity_scores)
    return "Sorry I do not understand" if max(cosine_similarity_scores)[0] < 0.41 else qna_list[max_index].answer