from typing import Union
import torch
import torch.nn as nn

LayerCollection = list[Union[nn.Linear, nn.ReLU]]


class RLModule(nn.Module):
    # TODO: Correctly move some components to device to sync
    def __init__(self, input_size: int, hidden_sizes: tuple[int], num_classes: int):
        super(RLModule, self).__init__()
        self.layers = LayerCollection()

        # Initialize layers
        prev_size = input_size
        end_size = num_classes

        for size in hidden_sizes:
            new_layer = nn.Linear(prev_size, size)
            self.layers.append(new_layer)
            self.layers.append(nn.ReLU())
            prev_size = size

        output_layer = nn.Linear(prev_size, end_size)
        self.layers.append(output_layer)

    def forward(self, x):
        for layer in self.layers:
            x = layer(x)
        return x
