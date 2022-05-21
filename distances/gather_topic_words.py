import re
from typing import List
import requests
import os
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


WORDS_API_URL = "https://api.datamuse.com/words?rel_trg="
WIKI_API_URL = "https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exlimit=1&explaintext=1&exsectionformat=plain&titles="
DOCUMENT_FILES_PATH = "document_words"


def gather_topic_words(topics: List[str], topic_files_path: str) -> None:
    for topic in topics:
        response = requests.get(WORDS_API_URL + topic).json()
        words = [el["word"] for el in response]
        words.append(topic)
        with open(os.path.join(topic_files_path, f"{topic}.data"), "w") as f:
            f.write("\n".join(words))


def parse_wiki_article(title: str) -> None:
    response = requests.get(WIKI_API_URL + title).json()["query"]["pages"].values()
    response = list(response)[0]["extract"]
    words = re.findall(r"[\w']+", response)

    words = [w.lower() for w in words if w.lower() not in ENGLISH_STOP_WORDS]

    doc_name = os.path.basename(title)
    with open(os.path.join(DOCUMENT_FILES_PATH, f"{doc_name}.data"), "w") as f:
        f.write("\n".join(words))


if __name__ == "__main__":
    os.makedirs(DOCUMENT_FILES_PATH, exist_ok=True)
    parse_wiki_article("memistor")
    topics = ["science", "sport", "shopping", "news"]
    gather_topic_words(topics, DOCUMENT_FILES_PATH)
