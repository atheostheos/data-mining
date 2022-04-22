import csv
import itertools
import os
from typing import List, Tuple


def calculate_pcy(transactions: List, support) -> Tuple[List[tuple], List[tuple]]:
    singletons = {}

    # add singletons
    for transaction in transactions:
        for prod in transaction:
            if prod not in singletons.keys():
                singletons[prod] = 1
            else:
                singletons[prod] += 1

    mapping_table = {}
    for i, item in enumerate(singletons):
        mapping_table[item] = i + 1
    hash_func = get_hash_func(mapping_table, len(mapping_table))

    # remove elements with small support
    for prod in list(singletons.keys()):
        if singletons[prod] < support:
            del singletons[prod]

    # get doublets
    doublet_candidates = generate_candidates(transactions)
    doublets = []
    bucket = {}

    # fill bucket
    for doublet in doublet_candidates:
        hv = hash_func(doublet)
        if hv not in bucket:
            bucket[hv] = [doublet]
        else:
            bucket[hv].append(doublet)

    # go through bucket, get only doublets with high support
    for doublet in set(doublet_candidates):
        hv = hash_func(doublet)
        count = len([1 for d in bucket[hv] if d == doublet])
        if count >= support:
            doublets.append(doublet)

    return list(singletons.keys()), doublets


def get_hash_func(mapping_table, mod):
    """
    Get hash for hash bucket
    """
    def _hash_func(itemset: Tuple[str]):
        return sum(map(mapping_table.get, itemset)) % mod

    return _hash_func


def generate_candidates(transactions: List[List[str]]) -> List[tuple]:
    """
    Generate doubleton candidates.
    :param transactions: List of transactions with name of products in them
    """
    candidates = []
    for transaction in transactions:
        comb = itertools.combinations(transaction, 2)
        candidates += map(tuple, comb)

    return candidates


if __name__ == "__main__":
    # read transactions data from file
    carts = {}
    with open("./files/transactions.csv", "r") as f:
        csv_reader = csv.reader(f, delimiter=";")
        next(csv_reader)
        for prod, cart in csv_reader:
            if cart not in carts.keys():
                carts[cart] = [prod]
            else:
                carts[cart].append(prod)

    transactions = list(carts.values())

    singletons, doublets = calculate_pcy(transactions, 2)

    # save itemsets to file
    os.makedirs("./pcy/", exist_ok=True)
    with open("./pcy/singletons.csv", "w") as f:
        csv.writer(f).writerows([s] for s in singletons)
    with open("./pcy/doublets.csv", "w") as f:
        csv.writer(f).writerows(doublets)

    print(f"Singletons amount: {len(singletons)}")
    print(f"Doublets amount: {len(doublets)}")
