import json
import os
import random
import re

from collections import Counter


class RaveGenerator:
    def __init__(self):
        self._BASE_DIR = os.path.dirname(__file__)

        self.tokens = self.get_tokens()
        self.model = self.get_model()

    def add_text(self, text):
        with open(f"{self._BASE_DIR}/data/rave.txt", 'a', encoding='utf-8') as f:
            tokens = re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
            new_text = '\n' + " ".join(tokens)
            f.write(new_text)

        self.tokens = self.get_tokens()
        self.update_model()

    def update_model(self):
        alpha = 0.8

        unigram_counts = Counter(self.tokens)
        bigram_counts = Counter((self.tokens[i], self.tokens[i + 1]) for i in range(len(self.tokens) - 1))
        total_unigrams = sum(unigram_counts.values())

        interpolated_probs = {}

        for (w1, w2), bigram_count in bigram_counts.items():
            p_bigram = bigram_count / unigram_counts[w1]
            p_unigram = unigram_counts[w2] / total_unigrams
            p_interp = alpha * p_bigram + (1 - alpha) * p_unigram

            if w1 not in interpolated_probs:
                interpolated_probs[w1] = {}

            interpolated_probs[w1][w2] = p_interp

        with open(f"{self._BASE_DIR}/data/interpolated_model.json", "w", encoding="utf-8") as f:
            json.dump(interpolated_probs, f, ensure_ascii=False, indent=4)

        self.model = self.get_model()

    def get_model(self):
        try:
            with open(f"{self._BASE_DIR}/data/interpolated_model.json", "r", encoding="utf-8") as file:
                model = json.load(file)
            return model
        except FileNotFoundError:
            raise "File not found."

    def get_tokens(self):
        try:
            with open(f"{self._BASE_DIR}/data/rave.txt", "r", encoding="utf-8") as file:
                text = file.read().replace("\n", " ")
                tokens = text.split()
            return tokens
        except FileNotFoundError:
            raise "File not found"

    def generate(self, start_word=None):
        length = random.randint(1, 20)

        if start_word is None:
            start_word = random.choice(self.tokens)

        result = [start_word]

        for _ in range(length):
            next_words = self.model.get(start_word)

            next_word = random.choices(
                population=list(next_words.keys()),
                weights=list(next_words.values())
            )[0]

            result.append(next_word)
            start_word = next_word

        return re.sub(r"\s+([.,!?;:%»])", r"\1", " ".join(result))


if __name__ == "__main__":
    rave = RaveGenerator()
    print(rave.generate())
