import os
import pickle
import nltk
import re
from typing import List
from lang_model import VOCAB_PATH
from lang_model.recognizer import LangRecognizer


class RecognizeLang:
    def __init__(self, model_name: str = "LSTM") -> None:
        # Vocalbulary
        self.__load_vocab()

        # Lookup table
        self.__construct_lookup()
        self.model = LangRecognizer(vocab_size=len(self.w2i))
        self.label_dict = {0: "Danish", 1: "Swedish", 2: "Norwegian"}

    def __load_vocab(self):
        path = os.path.join(VOCAB_PATH, "vocab.data")
        with open(path, "rb") as filehandle:
            self.vocab = pickle.load(filehandle)

    def __construct_lookup(self):
        self.w2i = {word: i for i, word in enumerate(self.vocab)}

    def recognize(self, text: str):
        # Lowercase and remove numbers
        text = re.sub(r"\d", "", text.lower())
        tokens = self._tokenize(text=text)

        # Get indexes from the vocalbulary
        input = [self.w2i[token] for token in tokens if token in self.w2i]

        # If none of the unput words are in the vocabulary, return error
        if input is None or len(input) == 0:
            raise ValueError("Words not recognized.")

        lang_index = self.model.predict(input)
        return self.label_dict[lang_index]

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        words = nltk.word_tokenize(text)
        tokens = [word for word in words if word.isalnum()]
        return tokens
