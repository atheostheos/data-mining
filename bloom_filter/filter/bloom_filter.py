import numpy as np
import math


class BloomFilter(object):

    def __init__(self, size: int, expected_number_of_elements: int):
        self.size = size

        self.filter = np.zeros((size,))

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
            self.filter[hash(word)] = 1

    def is_not_present(self, word: str):
        for hash in self.hashes:
            if self.filter[hash(word)] == 0:
                return True
        return False

    def is_present(self, word: str):
        return not self.is_not_present(word)


if __name__ == "__main__":
    bloom_filter = BloomFilter(100000, 600000)

    with open("../book-war-and-peace.txt", "r") as f:
        words = []
        for line in f:
            words += line.split()

    for word in words:
        bloom_filter.add_word(word)

    # present words
    print(bloom_filter.is_present("attained"))
    print(bloom_filter.is_present("who"))
    print(bloom_filter.is_present("bread"))

    # words not in set
    print(bloom_filter.is_present("hamburger"))
    print(bloom_filter.is_present("Yoko"))



