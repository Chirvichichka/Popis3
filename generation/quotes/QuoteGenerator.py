import os
import json
import random

from deep_translator import GoogleTranslator

def get_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_probabilities(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class QuoteGenerator:
    def __init__(self):
        self._BASE_DIR = os.path.dirname(__file__)

        self.text = get_text(f"{self._BASE_DIR}\\data\\quotes.txt")
        self.probabilities = get_probabilities(f"{self._BASE_DIR}\\data\\probabilities.json")

    def generate(self, length=10, random_param=True, language=None, start_word=None):
        if random_param:
            start_word = random.choice(self.text.split())
            length = random.randint(10, 30)

        current_word = start_word
        result = [current_word]

        for _ in range(length - 1):
            next_words = self.probabilities.get(current_word)
            if not next_words:
                break
            next_word = random.choices(
                population=list(next_words.keys()),
                weights=list(next_words.values()),
            )[0]
            result.append(next_word)
            current_word = next_word

        if language is None:
            quote = " ".join(result)
        else:
            quote = GoogleTranslator(source='en', target=language).translate(" ".join(result))
        return quote

if __name__ == "__main__":
    quote_generator = QuoteGenerator()
    quote = quote_generator.generate(language="ru")
    print(quote)
