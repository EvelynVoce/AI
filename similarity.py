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


def get_term_freq(word_dict, bag_of_words) -> dict:
    return {word:  (count / float(len(bag_of_words))) for (word, count) in word_dict.items()}


def get_num_of_words(bag_of_words_test, unique_words) -> dict:
    bag_of_words_test_lower: set[str] = {word.lower() for word in bag_of_words_test}
    num_of_words_test: dict = dict.fromkeys(unique_words, 0)
    for word in bag_of_words_test_lower:
        num_of_words_test[word] += 1
    return num_of_words_test


def get_all_term_freq(documents, unique_words) -> list[dict]:
    num_of_words: list[dict] = [get_num_of_words(document.split(), unique_words) for document in documents]
    return [get_term_freq(num_of_words[index], document.split()) for index, document in enumerate(documents)]


def get_idf(documents: list[dict]) -> dict:
    amount_of_docs: int = len(documents)

    idf_dict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, frequency in document.items():
            if frequency > 0:
                idf_dict[word] += 1

    for word, val in idf_dict.items():
        idf_dict[word]: float = log(amount_of_docs / val)

    return idf_dict


def get_tfidf(tf_bag_of_words, idfs) -> dict:
    return {word: (val * idfs[word]) for word, val in tf_bag_of_words.items()}


def get_similar(user_input: str) -> str:
    qna_list: list[QNAPair] = reading_csv()

    docs: list[str] = [q.question for q in qna_list]
    docs.append(user_input)  # Add the user input as the final document

    unique_words: set[str] = {word.lower() for document in docs for word in document.split()}
    tfs: list[dict] = get_all_term_freq(docs, unique_words)
    idfs: dict = get_idf([get_num_of_words(document.split(), unique_words) for document in docs])
    tfidfs: list[dict] = [get_tfidf(tf, idfs) for tf in tfs]

    df = pd.DataFrame(tfidfs)
    return calc_cos_similarity(df, qna_list)


def calc_cos_similarity(df, qna_list) -> str:
    cosine_similarity_scores: list[list[int]] = cosine_similarity(df.iloc[:-1], df.iloc[-1:])
    max_index = argmax(cosine_similarity_scores)
    print(max(cosine_similarity_scores)[0])
    if max(cosine_similarity_scores)[0] < 0.41:  # If no similarity
        return "Sorry I do not understand"
    return qna_list[max_index].answer

# Input_counts
#     input_counts = []
#     for word in bag_of_words:
#         value = 0
#         for input_word in user_input.split():
#             if word == input_word:
#                 value += 1
#         input_counts.append(value / len(user_input.split()))
#
#     cosine_similarity_scores: list[int] = [cosine_similarity([tf_idf], [input_counts])
#                                            for tf_idf in list_of_tf_idf]



# def get_similar(user_input) -> str:
#     qna_list: list[QNAPair] = reading_csv()
#     bag_of_words = set(user_input.split())
#
#     words_in_question = np.array([[word.lower() for word in x.question.split()] for x in qna_list], dtype=object)
#     # word_in_sentence: list[list[int]] = [[1 if word_in_bag in word_in_question else 0 for word_in_bag in bag_of_words]
#     #                                      for word_in_question in words_in_question]
#
#     # TF
#     word_in_sentence: list[list[float]] = []
#     for word_in_question in words_in_question:
#         temp = []
#         for word in bag_of_words:
#             value = 0
#             for x in word_in_question:
#                 if word == x:
#                     value += 1
#             temp.append(value / len(words_in_question))
#         word_in_sentence.append(temp)  # Term frequency
#
#     # IDF
#     idf = []
#     total_questions = len(words_in_question)
#     for word_in_question in words_in_question:
#         frequency = 0
#         for word in word_in_question:
#             if word in word_in_question:
#                 frequency += 1
#         idf.append(log(total_questions/frequency))
#
#     # TF-IDF
#     list_of_tf_idf = [np.multiply(np.array(word_in_sentence[x]),
#                                   np.array(idf[x])) for x in range(len(word_in_sentence))]
#     df = pd.DataFrame(list_of_tf_idf)
#     print(df)
#
#     # Input_counts
#     input_counts = []
#     for word in bag_of_words:
#         value = 0
#         for input_word in user_input.split():
#             if word == input_word:
#                 value += 1
#         input_counts.append(value / len(user_input.split()))
#
#     cosine_similarity_scores: list[int] = [cosine_similarity([tf_idf], [input_counts])
#                                            for tf_idf in list_of_tf_idf]
#
#     # cosine_similarity_scores: list[int] = [cosine_similarity([sentence], [input_counts])
#     #                                      for sentence in word_in_sentence]
#
#     if max(cosine_similarity_scores) == 0:
#         return "Sorry I do not understand"
#
#     for index, score in enumerate(cosine_similarity_scores):
#         if score == max(cosine_similarity_scores):
#             return qna_list[index].answer
