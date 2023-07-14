import torch
import torch.nn as nn

from autoagent import AutoAgent
from rlmodule import RLModule

import numpy as np
from collections import namedtuple, deque
from itertools import count


class TensorAgent(AutoAgent):
    def __init__(self, input_size: int, hidden_sizes: tuple[int]):
        output_size = 2
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._model = RLModule(input_size, hidden_sizes, output_size).to(self.device)

    def get_action(self, state: np.array):
        """Given the state of the game, model predicts True to jump or False to stay idle."""
        state_t = torch.from_numpy(state).float().to(self.device)
        logits = self._model(state_t)
        pred_probab = nn.Softmax(dim=1)(logits)
        # We get the most activated output node
        choice = torch.argmax(pred_probab)
        # choice = 0 -> no jump
        # choice = 1 -> jump
        return choice == 1

    def draw_debug(self, surface, scale):
        pass
