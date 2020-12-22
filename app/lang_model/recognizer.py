import os
import torch
import torch.nn as nn
from lang_model import DATA_PATH
from lang_model.model import LangModel


class LangRecognizer:
    def __init__(self, vocab_size: int, name: str = "LSTM") -> None:
        self.path = os.path.join(DATA_PATH, "models", name)
        self.vocab_size = vocab_size
        self.__load_model()

    def __load_model(self) -> None:
        models = list(filter(lambda x: x.endswith(".pt"), os.listdir(self.path)))
        if len(models) == 0:
            raise ValueError("Wrong path.")

        state_dict = torch.load(os.path.join(self.path, models[0]))
        self.model = LangModel(self.vocab_size)
        self.model.load_state_dict(state_dict)
        self.model.eval()

    def predict(self, data) -> str:
        # Convert to tensor
        input = torch.Tensor(data).long()

        # Add batch and input to model
        output = self.model(input.unsqueeze(0))

        # Get outputs
        _, pred = torch.max(output["out"].detach(), 1)

        # Convert to Language name
        lang_code = int(pred.detach().numpy()[0])
        return lang_code