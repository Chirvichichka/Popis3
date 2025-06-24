import json
import os
import random

from deep_translator import GoogleTranslator


def get_probabilities(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_text(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


class NewsGenerator:
    def __init__(self):
        self._BASE_DIR = os.path.dirname(__file__)
        self.text = get_text(f"{self._BASE_DIR}\\data\\news_text.txt")
        self.probabilities = get_probabilities(f"{self._BASE_DIR}\\data\\probabilities.json")

    def generate(self, length=None, language='en', start_word=None):
        if not length:
            length = random.randint(10, 30)

        if start_word in self.probabilities.keys():
            current_word = start_word
        else:
            current_word = random.choice(self.text.split())

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

        if language == 'en':
            news = " ".join(result)
        else:
            news = GoogleTranslator(source='en', target=language).translate(" ".join(result))
        return news


if __name__ == "__main__":
    news_generator = NewsGenerator()
    news = news_generator.generate(language="ru")
    print(news)
