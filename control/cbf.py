import numpy as np
import math


class BloomFilter(object):

    def __init__(self, size: int, expected_number_of_elements: int):
        self.size = size

        self.filter = np.zeros((size,), dtype=int)

        self.hash_num = math.ceil(self.size / expected_number_of_elements * math.log(2))
        self.hashes = [self._make_hash(str(i)) for i in range(self.hash_num)]

    def _make_hash(self, salt: str):
        def hash_djb2_salted(word):
            word = salt + word
            hash = 5381
            for letter in word:
                hash = ((hash << 5) + hash) + ord(letter)
            return hash % self.size

        return hash_djb2_salted

    def add_word(self, word: str):
        for hash in self.hashes:
            self.filter[hash(word)] += 1

    def is_not_present(self, word: str):
        for hash in self.hashes:
            if self.filter[hash(word)] == 0:
                return True
        return False

    def is_present(self, word: str):
        return not self.is_not_present(word)


if __name__ == "__main__":

    with open("./files/cbf.txt", "r") as f:
        words = []
        for line in f:
            words += [w.strip(",!.-:").lower() for w in line.split()]

    expected_number_of_elements = len(set(words))

    # (1) k = n/m * ln2
    # (2) P(FP) = (1 - e^(-k*m/n))^k
    # (1) -> (2): P(FP) = (1-e^(ln2))^(n/m*ln2) = 0.5^n/m*ln2), P(FP) = 0.1, m = 34 =>
    # log_{0.5}(0.1)= n*m/ln2
    # n = ~16

    bloom_filter = BloomFilter(16, expected_number_of_elements)

    for word in words:
        bloom_filter.add_word(word)

    print(bloom_filter.filter)
    print(f"Number of hashes: {bloom_filter.hash_num}")
    print()
