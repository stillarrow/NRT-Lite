from torch import nn
from .mlp import MLP


class Rater(nn.Module):
    '''
    Multilayer Perceptron

    Inputs:
        input_var: shape=(batch_size, d_ui)

    Outputs:
        output_var: shape=(batch_size)
    '''

    def __init__(
        self,
        d_input,
        layer_sizes,
        **kargs
    ):
        super(Rater, self).__init__()

        self.mlp = MLP(d_input, layer_sizes, **kargs)

        # Add a linear layer after the final layer of MLP
        self.output = nn.Linear(layer_sizes[-1], 1)

        # self.to_rating = nn.Sequential(
        #     nn.Sigmoid(),
        #     nn.Linear(1, 1)
        # )

        # self.to_logit = nn.Sequential(
        #     nn.Linear(1, 1)
        # )

    def forward(self, input_var):
        output_var = self.mlp(input_var)
        ratings = self.output(output_var)
        ratings = ratings.squeeze(1)

        return ratings
