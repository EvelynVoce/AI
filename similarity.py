import csv
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from math import log

class QNAPair:
    def __init__(self, row):
        self.question: str = row[0]
        self.answer: str = row[1]


def reading_csv() -> list[str]:
    with open("knowledge.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # Skip the first line because it's just the headings for the columns
        return [QNAPair(row) for row in csv_reader]


def get_term_freq(wordDict, bagOfWords) -> dict:
    return {word:  (count / float(len(bagOfWords))) for (word, count) in wordDict.items()}


def get_num_of_words(bagOfWordsTest, uniqueWords):
    numOfWordsTest = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWordsTest:
        numOfWordsTest[word] += 1
    return numOfWordsTest


def tf_func(documents):
    uniqueWords = {word for document in documents for word in document.split()}
    num_of_words = [get_num_of_words(document.split(), uniqueWords) for document in documents]
    tfs = [get_term_freq(num_of_words[index], document.split()) for index, document in enumerate(documents)]
    return tfs


def get_idf(documents):
    amount_of_docs: int = len(documents)

    idf_dict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, fequency in document.items():
            if fequency > 0:
                idf_dict[word] += 1

    for word, val in idf_dict.items():
        idf_dict[word]: float = log(amount_of_docs / val)

    return idf_dict


def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf


def get_similar(user_input) -> str:
    qna_list: list[QNAPair] = reading_csv()
    docs = [q.question for q in qna_list]
    docs.append(user_input) # Add the user input as the final document
    uniqueWords = {word for document in docs for word in document.split()}
    tfs = tf_func(docs)
    idfs = get_idf([get_num_of_words(document.split(), uniqueWords) for document in docs])
    tfidfs = [computeTFIDF(tf, idfs) for tf in tfs]
    df = pd.DataFrame(tfidfs)

    # Cosine similarity
    cosine_similarity_scores: list[int] = cosine_similarity(df.iloc[:-1], df.iloc[-1:])
    largest = 0
    largest_index = 0
    for index, data in enumerate(cosine_similarity_scores):
        if data[0] > largest:
            largest = data[0]
            largest_index = index

    if largest == 0:
        return "Sorry I do not understand"
    return qna_list[largest_index].answer

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
