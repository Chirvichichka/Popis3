import json
import os
import random
from collections import defaultdict, Counter

from deep_translator import GoogleTranslator


def get_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_probabilities(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def init_model(text):
    model = defaultdict(Counter)
    words = text.lower().split()

    for i in range(len(words) - 2):
        w1, w2, w3 = words[i], words[i + 1], words[i + 2]
        model[(w1, w2)][w3] += 1

    return model


class QuoteGenerator:
    def __init__(self):
        self._BASE_DIR = os.path.dirname(__file__)

        self.text = get_text(f"{self._BASE_DIR}\\data\\quotes.txt")
        self.average_length = self.calculate_average_length()

        self.model = init_model(self.text)

    def calculate_average_length(self):
        with open(f"{self._BASE_DIR}\\data\\quotes.json", "r", encoding="utf-8") as f:
            quotes = json.load(f)

        sentences = [sent["Quote"] for sent in quotes]

        all_length = [len(sent.split()) for sent in sentences]
        average_length = sum(all_length) / len(sentences)

        return int(average_length)

    def generate(self, length=None, language=None, start_pair=None):
        """Если start_word == None, то будет выбрано случайное слово из вокабуляра"""
        if length is None:
            length = self.average_length

        if start_pair is None:
            start_pair = random.choice(list(self.model.keys()))

        w1, w2 = start_pair
        result = [w1, w2]
        for _ in range(length):
            next_word_options = self.model.get((w1, w2))
            if not next_word_options:
                break
            w3 = random.choices(
                population=list(next_word_options.keys()),
                weights=list(next_word_options.values())
            )[0]
            result.append(w3)
            w1, w2 = w2, w3

        if language is None:
            quote = " ".join(result)
        else:
            quote = GoogleTranslator(source='en', target=language).translate(" ".join(result))
        return quote


if __name__ == "__main__":
    quote_generator = QuoteGenerator()
    quote = quote_generator.generate()
    print(quote)
