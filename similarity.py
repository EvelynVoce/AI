import csv
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class QNAPair:
    def __init__(self, row):
        self.question: str = row[0]
        self.answer: str = row[1]


def reading_csv() -> list[str]:
    with open("knowledge.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # Skip the first line because it's just the headings for the columns
        return [QNAPair(row) for row in csv_reader]


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


def get_similar(user_input) -> str:
    qna_list: list[QNAPair] = reading_csv()
    docs = [q.question for q in qna_list]
    docs.append(user_input) # Add the user input as the final document
    uniqueWords = {word for document in docs for word in document.split()}
    tfs = tf_func(docs)
    idfs = computeIDF([get_num_of_words(document.split(), uniqueWords) for document in docs])
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
