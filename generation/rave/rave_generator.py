import json
import os
import random
import re

from collections import defaultdict, Counter

_BASE_DIR = os.path.dirname(__file__)


def load_text():
    with open(f"{_BASE_DIR}\\data\\rave.txt", 'r', encoding='utf-8') as f:
        return f.read().replace('\n', ' ').strip()


def load_probabilities(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


class RaveGenerator:
    def __init__(self):
        self.text = load_text()
        self.probabilities = load_probabilities(path=f"{_BASE_DIR}\\data\\probabilities.json")

    def update_probabilities(self):
        transitions = defaultdict(list)
        text = self.text.split()

        for i in range(len(text) - 2):
            w1, w2 = text[i], text[i + 1]
            next_word = text[i + 2]
            transitions[(w1, w2)].append(next_word)

        for key, next_words in transitions.items():
            total = len(next_words)
            counter = Counter(next_words)
            key_str = ' '.join(key)
            self.probabilities[key_str] = {word: count / total for word, count in counter.items()}

        with open(f"{_BASE_DIR}\\data\\probabilities.json", "w", encoding="utf-8") as f:
            json.dump(self.probabilities, f, ensure_ascii=False, indent=4)

    def update_text(self):
        self.text = load_text()

    def add_text(self, text):
        with open(f"{_BASE_DIR}\\data\\rave.txt", 'a', encoding='utf-8') as f:
            tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
            if tokens[-1] not in re.findall(r"[^\w\s]", text, re.UNICODE):
                tokens.append(".")
            new_text = '\n' + " ".join(tokens)
            f.write(new_text)

        self.update_text()
        self.update_probabilities()

    def generate(self, length=None):
        if length is None:
            length = random.randint(1, 20)

        start = random.choices(list(self.probabilities.keys()))
        w1, w2 = start[0].split(' ')

        result = [w1, w2]
        for _ in range(length):
            next_words = self.probabilities.get(f"{w1} {w2}")

            if not next_words:
                break

            w3 = random.choices(
                population=list(next_words.keys()),
                weights=list(next_words.values())
            )[0]

            result.append(w3)
            w1, w2 = w2, w3

        return re.sub(r"\s+([.,!?;:%»])", r"\1", " ".join(result))


if __name__ == "__main__":
    rave = RaveGenerator()
    rave.update_probabilities()
    k = rave.probabilities.keys()
    print(k)
    r = rave.generate()
    print(load_text())
    print(r)
