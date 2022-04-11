import typing as tp
import lorem


class TextGenerator:
    @staticmethod
    def generate_question_text(number_of_words: int) -> str:
        text = TextGenerator.generate_text(number_of_words)
        return f"{text[:-1]}?" # Remove period and add question mark

    @staticmethod
    def generate_text(number_of_words: int) -> str:
        return " ".join(TextGenerator._generate_words(number_of_words))

    @staticmethod
    def _generate_words(number_of_words: int, as_senteces: bool = True) -> tp.List[str]:
        words = []
        while len(words) < number_of_words:
            if as_senteces:
                words.extend(lorem.sentence().split(" "))
            else:
                words.extend(lorem.text().split(" "))
        words = words[:number_of_words]
        if not words[-1].endswith('.'):
            words[-1] = f"{words[-1]}." # Add period on the end of the last sentence
        return words
