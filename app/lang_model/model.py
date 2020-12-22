import torch
import torch.nn as nn
from torch.nn.functional import softmax


class LangModel(nn.Module):
    def __init__(self, vocab_size):
        super(LangModel, self).__init__()
        self.embeddings = nn.Embedding(vocab_size, 32)

        self.rnn_1 = nn.LSTM(
            input_size=32,
            hidden_size=100,
            num_layers=2,
            bidirectional=True,
            batch_first=False,
        )

        self.l_out = nn.Sequential(
            nn.Linear(400, 200),
            nn.Dropout(0.2),
            nn.ReLU(inplace=True),
            nn.Linear(200, 64),
            nn.ReLU(inplace=True),
            nn.BatchNorm1d(64),
            nn.Linear(64, 3),
        )

    def forward(self, x):
        out = {}

        # get embeddings
        x = self.embeddings(x)

        # output, hidden state
        x, _ = self.rnn_1(x)

        x = torch.cat((torch.mean(x, dim=0), torch.max(x, dim=0)[0]), dim=1)

        # classify
        out["out"] = softmax(self.l_out(x), dim=1)
        print(out)
        return out