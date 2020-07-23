#
# Heuristic using features generated for generalized planning
#

"""
Landmarks Heuristic
"""

import torch
from heuristics.GPfeatures_NN import GP_NN_heuristic_model_class,trained_model_location
from heuristics.heuristic_base import Heuristic


def compute_NN_wGPF_heuristic(task):
    #unpickle the saved model, and do inference
    nn_model = torch.load(trained_model_location)
    #todo extract state from task, pass the state information to the lisp program and get the GP features.
    # then do inference with the NN model, and return the result
    pass


class GPfeaturesHeuristic(Heuristic): #class name must end with "Heuristic"
    def __init__(self, task):
        self.task = task


    def __call__(self, node):
        """ Returns the heuristic value for "node". """
        h = compute_NN_wGPF_heuristic(node)
        h = 1.0
        #For nodes that are known to be deadends (i.e. there is no valid plan that
        # reaches the goal from this node), a heuristic value of `float('inf')` should
        # be returned.
        return h
