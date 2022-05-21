import os
from typing import List
import numpy as np
from numpy.linalg import norm
import glob

DOCUMENTS_DIR_PATH = "document_words"


def calculate_jaccard_index(elements: List[List[str]]) -> np.ndarray:
    """
        Calculate jaccard indexes for selected elements
        :param elements: list of elements' document_words
        :return: matrix of relations, index of matrix is same as index in provided list
        """
    s = len(elements)
    matrix = np.zeros(dtype=float, shape=(s, s))
    el_sets = [set(el) for el in elements]
    for i in range(s):
        for j in range(s):
            if i == 1:
                print(el_sets[j].intersection(el_sets[i]))
            matrix[i][j] = len(el_sets[j].intersection(el_sets[i])) / len(el_sets[i].union(el_sets[j]))

    return matrix


def calculate_cosine_metrics(elements: List[List[str]]) -> np.ndarray:
    """
    Calculate cosine metrics for selected elements
    :param elements: list of elements' document_words
    :return: matrix of relations, index of matrix is same as index in provided list
    """
    # get list of all unique document_words
    unique_words = []
    for element in elements:
        unique_words += element
    unique_words = list(set(unique_words))
    print(f"Total amount of unique document_words: {len(unique_words)}")

    # make vectors
    vectors = []
    for element in elements:
        vector = []
        for word in unique_words:
            amount = len(list(filter(lambda w: w == word, element)))
            vector.append(amount)
        vectors.append(vector)

    # calculate cosine distances
    s = len(vectors)
    matrix = np.zeros(dtype=float, shape=(s, s))
    for i in range(s):
        for j in range(s):
            matrix[i][j] = np.dot(vectors[i], vectors[j])/(norm(vectors[i])*norm(vectors[j]))

    return matrix


if __name__ == "__main__":
    documents = glob.glob(f"{DOCUMENTS_DIR_PATH}/*.data")
    document_words = []
    for document in documents:
        with open(document, "r") as f:
            words = [w.strip("\n ").lower() for w in f.readlines()]
            document_words.append(words)

    names = [os.path.basename(d).replace(".data", "") for d in documents]
    print(f"Documents_list: {names}")
    print("Jaccard metrics:")
    print(calculate_jaccard_index(document_words))
    print("Cosine metrics:")
    print(calculate_cosine_metrics(document_words))


