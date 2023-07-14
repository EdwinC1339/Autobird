from abc import ABC, abstractmethod
import numpy as np


class AutoAgent(ABC):
    @abstractmethod
    def get_action(self, state: np.array):
        """Given the state of the game, model predicts True to jump or False to stay idle."""
        pass

    @abstractmethod
    def draw_debug(self, surface, scale):
        pass
