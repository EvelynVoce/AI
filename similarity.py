import csv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


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
    bag_of_words = set(user_input.split())

    words_in_question = np.array([[word.lower() for word in x.question.split()] for x in qna_list], dtype=object)

    # TF
    word_in_sentence: list[list[float]] = []
    for word_in_question in words_in_question:
        temp = []
        for word in bag_of_words:
            value = 0
            for x in word_in_question:
                if word == x:
                    value += 1
            temp.append(value / len(words_in_question))
        word_in_sentence.append(temp)  # Term frequency

    # Input_counts
    input_counts = []
    for word in bag_of_words:
        value = 0
        for input_word in user_input.split():
            if word == input_word:
                value += 1
        input_counts.append(value / len(user_input.split()))

    cosine_similarity_scores: list[int] = [cosine_similarity([sentence], [input_counts])
                                           for sentence in word_in_sentence]

    if max(cosine_similarity_scores) == 0:
        return "Sorry I do not understand"

    for index, score in enumerate(cosine_similarity_scores):
        if score == max(cosine_similarity_scores):
            return qna_list[index].answer
