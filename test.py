import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from math import log
from sklearn.feature_extraction.text import TfidfVectorizer

class QNAPair:
    def __init__(self, row):
        self.question: str = row[0]
        self.answer: str = row[1]


def reading_csv() -> list[str]:
    with open("knowledge.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # Skip the first line because it's just the headings for the columns
        return [QNAPair(row) for row in csv_reader]


def get_similar(user_input) -> str:
    qna_list: list[QNAPair] = reading_csv()
    bag_of_words = user_input.split()  # Gets rid of duplicates (but duplicates are kinda important
    bag_of_words = np.array(bag_of_words)

    words_in_question = np.array([[word.lower() for word in x.question.split()] for x in qna_list], dtype=object)

    word_in_sentence: list[list[int]] = [[1 if word_in_bag in word_in_question else 0 for word_in_bag in bag_of_words]
                                         for word_in_question in words_in_question]

    array_of_ones = np.ones(len(bag_of_words))
    print(array_of_ones)

    cosine_similarity_scores: list[int] = [cosine_similarity([sentence], [array_of_ones])
                                           for sentence in word_in_sentence]

    if max(cosine_similarity_scores) == 0:
        return "Sorry I do not understand"

    for index, score in enumerate(cosine_similarity_scores):
        if score == max(cosine_similarity_scores):
            return qna_list[index].answer


# from nltk import word_tokenize, pos_tag
# def test():
#     sentence: str = input("Enter a sentence")
#
#     tokens: list[str] = word_tokenize(sentence)
#     tagged: tuple[(str, str)] = pos_tag(tokens)
#     print(tagged)
#
#
# def get_tf_idf():
#     str1 = "the sky is blue"
#     str2 = "the sky is not blue"
#
#     tf1 = [1, 1, 1, 1, 0]
#     tf2 = [1, 1, 1, 1, 1]
#
#     # idf = [log(2/2), log(2/2), log(2/2), log(2/2), log(2/1)]
#
#     # tfidf1 = tf1*idf
#     # tfidf2 = tf2*idf
#
#
#
#     str1 = "the sky is blue"
#     str2 = "the sky is not sky"
#
#     # [the, sky, is, blue, not]
#     tf1 = [1, 1, 1, 1, 0]
#     tf2 = [1, 2, 1, 1, 1]
#
# # Doesn't appear to work
# def get_tf_idf2(answer):
#     vectorizer = TfidfVectorizer()
#     response = vectorizer.fit_transform(["the", "tenth", "doctor"], ["the", "ninth", "doctor"])
#     print("response\n", response)

    # IDF
    idf = []
    total_questions = len(words_in_question)
    for word_in_question in words_in_question:
        frequency = 1
        for word in bag_of_words:
            if word in word_in_question:
                frequency += 1
        idf.append(log(total_questions/frequency))

        # TF-IDF
        list_of_tf_idf = [np.multiply(np.array(word_in_sentence[x]), np.array(idf[x])) for x in range(word_in_sentence)]

        cosine_similarity_scores: list[int] = [cosine_similarity([tf_idf], [input_counts])
                                               for tf_idf in list_of_tf_idf]
