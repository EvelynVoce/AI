import pandas as pd

def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict


def get_num_of_words(bagOfWordsTest, uniqueWords):
    numOfWordsTest = dict.fromkeys(uniqueWords, 0)
    for word in bagOfWordsTest:
        numOfWordsTest[word] += 1
    return numOfWordsTest


def tf_func(documents):
    # Scalable solution
    uniqueWords = {word for document in documents for word in document.split()}
    num_of_words = [get_num_of_words(document.split(), uniqueWords) for document in documents]
    tfs = [computeTF(num_of_words[index], document.split()) for index, document in enumerate(documents)]
    tf = pd.DataFrame(tfs)
    print(tf)
    return tfs


def computeIDF(documents):
    import math
    amount_of_docs = len(documents)

    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in documents:
        for word, fequency in document.items():
            if fequency > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log(amount_of_docs / int(val))

    idfs = pd.DataFrame([idfDict])
    print(idfs)
    return idfDict


def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf


import csv


class QNAPair:
    def __init__(self, row):
        self.question: str = row[0]
        self.answer: str = row[1]


def reading_csv() -> list[str]:
    with open("knowledge.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # Skip the first line because it's just the headings for the columns
        return [QNAPair(row) for row in csv_reader]


def main():
    docs = ["Jupiter is the largest planet", "Mars is the fourth planet from the sun",
            "Test string very big", "Big book me read smart", "Will this work"]
    docs = reading_csv()

    answer = "big very"
    answer = input("> ")
    docs.append(answer)

    tfs = tf_func(docs)
    uniqueWords = {word for document in docs for word in document.split()}
    idfs = computeIDF( [get_num_of_words(document.split(), uniqueWords) for document in docs] )

    tfidfs = [computeTFIDF(tf, idfs) for tf in tfs]
    df = pd.DataFrame(tfidfs)

    from sklearn.metrics.pairwise import cosine_similarity
    cosine_similarity_scores: list[int] = cosine_similarity(df.iloc[:-1], df.iloc[-1:])
    df = pd.DataFrame(cosine_similarity_scores)

    largest = 0
    largest_index = 0
    for index, data in enumerate(cosine_similarity_scores):
        if data[0] > largest:
            largest = data[0]
            largest_index = index

    if largest == 0:
        return "Sorry I do not understand"

    return docs[largest_index]

main()


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


# from sklearn.feature_extraction.text import TfidfVectorizer
#
# vectorizer = TfidfVectorizer()
# docs = ["Jupiter is the largest planet", "Mars is the fourth planet from the sun"]
#
# vectors = vectorizer.fit_transform(docs)
# feature_names = vectorizer.get_feature_names()
# dense = vectors.todense()
# denselist = dense.tolist()
# df = pd.DataFrame(denselist, columns=feature_names)
# print(df)


#
# def computeTF(wordDict, bagOfWords):
#     tfDict = {}
#     bagOfWordsCount = len(bagOfWords)
#     for word, count in wordDict.items():
#         tfDict[word] = count / float(bagOfWordsCount)
#     return tfDict
#
# documentA = "Jupiter is the largest planet"
# documentB = "Mars is the fourth planet from the sun"
#
# bagOfWordsA = documentA.split(' ')
# bagOfWordsB = documentB.split(' ')
#
# uniqueWords = set(bagOfWordsA).union(set(bagOfWordsB))
#
# numOfWordsA = dict.fromkeys(uniqueWords, 0)
# for word in bagOfWordsA:
#     numOfWordsA[word] += 1
# numOfWordsB = dict.fromkeys(uniqueWords, 0)
# for word in bagOfWordsB:
#     numOfWordsB[word] += 1
#
# df = pd.DataFrame([numOfWordsA, numOfWordsB])
# # print(df)
#
# tfA = computeTF(numOfWordsA, bagOfWordsA)
# tfB = computeTF(numOfWordsB, bagOfWordsB)
# tf = pd.DataFrame([tfA, tfB])
# print(tf)










# import csv
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from math import log
# from sklearn.feature_extraction.text import TfidfVectorizer
#
# class QNAPair:
#     def __init__(self, row):
#         self.question: str = row[0]
#         self.answer: str = row[1]
#
#
# def reading_csv() -> list[str]:
#     with open("knowledge.csv") as csv_file:
#         csv_reader = csv.reader(csv_file, delimiter=',')
#         next(csv_reader)  # Skip the first line because it's just the headings for the columns
#         return [QNAPair(row) for row in csv_reader]
#
#
#
# # Doesn't appear to work
# def get_tf_idf2(answer):
#     corpus = reading_csv()
#     vectorizer = TfidfVectorizer()
#     response = vectorizer.fit_transform([q.question for q in corpus])
#     print("response\n", response)
#
#
# def get_similar(user_input) -> str:
#     qna_list: list[QNAPair] = reading_csv()
#     bag_of_words = user_input.split()  # Gets rid of duplicates (but duplicates are kinda important
#     bag_of_words = np.array(bag_of_words)
#
#     words_in_question = np.array([[word.lower() for word in x.question.split()] for x in qna_list], dtype=object)
#
#     word_in_sentence: list[list[int]] = [[1 if word_in_bag in word_in_question else 0 for word_in_bag in bag_of_words]
#                                          for word_in_question in words_in_question]
#
#     array_of_ones = np.ones(len(bag_of_words))
#     print(array_of_ones)
#
#     cosine_similarity_scores: list[int] = [cosine_similarity([sentence], [array_of_ones])
#                                            for sentence in word_in_sentence]
#
#     if max(cosine_similarity_scores) == 0:
#         return "Sorry I do not understand"
#
#     for index, score in enumerate(cosine_similarity_scores):
#         if score == max(cosine_similarity_scores):
#             return qna_list[index].answer
#
#
# # from nltk import word_tokenize, pos_tag
# # def test():
# #     sentence: str = input("Enter a sentence")
# #
# #     tokens: list[str] = word_tokenize(sentence)
# #     tagged: tuple[(str, str)] = pos_tag(tokens)
# #     print(tagged)
# #
# #
# # def get_tf_idf():
# #     str1 = "the sky is blue"
# #     str2 = "the sky is not blue"
# #
# #     tf1 = [1, 1, 1, 1, 0]
# #     tf2 = [1, 1, 1, 1, 1]
# #
# #     # idf = [log(2/2), log(2/2), log(2/2), log(2/2), log(2/1)]
# #
# #     # tfidf1 = tf1*idf
# #     # tfidf2 = tf2*idf
# #
# #
# #
# #     str1 = "the sky is blue"
# #     str2 = "the sky is not sky"
# #
# #     # [the, sky, is, blue, not]
# #     tf1 = [1, 1, 1, 1, 0]
# #     tf2 = [1, 2, 1, 1, 1]
# #
# # # # Doesn't appear to work
# def get_tf_idf2():
#     corpus = ["Jupiter is the largest planet", "Mars is the fourth planet from the sun"]
#     vectorizer = TfidfVectorizer(smooth_idf=True)
#     response = vectorizer.fit_transform([q for q in corpus])
#     df = pd.DataFrame(response)
#     print(df)
#
#     # IDF
#     idf = []
#     total_questions = len(words_in_question)
#     for word_in_question in words_in_question:
#         frequency = 1
#         for word in bag_of_words:
#             if word in word_in_question:
#                 frequency += 1
#         idf.append(log(total_questions/frequency))
#
#         # TF-IDF
#         list_of_tf_idf = [np.multiply(np.array(word_in_sentence[x]), np.array(idf[x])) for x in range(word_in_sentence)]
#
#         cosine_similarity_scores: list[int] = [cosine_similarity([tf_idf], [input_counts])
#                                                for tf_idf in list_of_tf_idf]





# def computeTF(wordDict, bagOfWords):
#     tfDict = {}
#     bag_of_words_length = len(bagOfWords)
#     for word, count in wordDict.items():
#         tfDict[word] = count / float(bag_of_words_length)
#     return tfDict
