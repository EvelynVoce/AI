from nltk.corpus import wordnet as wn
from itertools import chain


def main():
    test_input: str = "The quick brown fox"
    kb: str = ["A fast brown animal", 'quick man jumps fox']

    input_words: set[str] = set(test_input.split())

    bag_of_bags: set[set[str]] = []
    for word in input_words:
        synonyms = [synonym.lemma_names() for synonym in wn.synsets(word)]
        if not synonyms:
            synonyms.append(["The"])
        similar_words = set(chain.from_iterable(synonyms))
        bag_of_bags.append(similar_words)
    print(bag_of_bags)

    words = []
    for k in kb:
        words_in_k = []
        for bag in bag_of_bags:
            for word in bag:
                if word in k:
                    words_in_k.append(word)
                    break
        words.append(words_in_k)
    print(words)


if __name__ == "__main__":
    main()
