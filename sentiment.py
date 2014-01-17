import pattern.en
from pattern.en import Sentence, parse, modality


class TextSentiment:
    """
        wrapper to pattern.en sentiment implementation
        """

    def __init__(self, text):
        self.text = text
        self.get_sentiment(self.text)

    def __str__(self):
        return self.text

    def get_sentiment(self, text):
        self.polarity, self.subjectivity = pattern.en.sentiment(text)

    def get_modality(self, text):
        s = Sentence(parse(text, chunks=False, lemmata=True))
        self.modality = pattern.en.modality(s)

if __name__ == '__main__':
    # test code   
    sentences = [
        "I am very happy with this service. I hope I can get the newest version",
        "I hate going to that park. It sucks!",
        "Well, I don't know about that, maybe another time",
        "One of the coolest things i've ever seen. What a moment!"]
    ts_sentences = [TextSentiment(sentence) for sentence in sentences]
