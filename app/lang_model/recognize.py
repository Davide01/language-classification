import os
import pickle
import nltk
import re
import numpy as np
from typing import List
from sklearn import preprocessing
from lang_model import VOCAB_PATH, ENCODER_PATH
from lang_model.recognizer import LangRecognizer
from lang_model.utils import map_language_code


class RecognizeLang:
    def __init__(self, model_name: str = "lstm") -> None:
        # Vocalbulary
        self.__load_vocab()

        # Lookup table
        self.__construct_lookup()
        self.model = LangRecognizer(vocab_size=len(self.w2i), name=model_name)
        self.__load_encoder()

    def __load_vocab(self):
        path = os.path.join(VOCAB_PATH, "vocab.data")
        with open(path, "rb") as filehandle:
            self.vocab = pickle.load(filehandle)

    def __construct_lookup(self):
        self.w2i = {word: i for i, word in enumerate(self.vocab)}

    def __load_encoder(self):
        self.label_encoder = preprocessing.LabelEncoder()
        self.label_encoder.classes_ = np.load(os.path.join(ENCODER_PATH, "encoder_classes.npy"), allow_pickle=True)

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
        language_code = self.label_encoder.inverse_transform([lang_index])
        return map_language_code(language_code[0])

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        words = nltk.word_tokenize(text)
        tokens = [word for word in words if word.isalnum()]
        return tokens
