#
# Heuristic using features generated for generalized planning
#

"""
Landmarks Heuristic
"""

import torch
from heuristics.heuristic_base import Heuristic
from heuristics.GenPlan_HeuristicSupport.Gripper_GPfeatures_NN import trained_model_location

# The following line is because the cwd from which this file is called is the src directory
trained_model_location = "./heuristics/GenPlan_HeuristicSupport/" + trained_model_location

def compute_NN_wGPF_heuristic(state_frozen_set_proposition_strings):
    #unpickle the saved model, and do inference
    nn_model = torch.load(trained_model_location)

    FIRST make sure you were training with sensible things. the numbers being spewed, that is the cost, yes ? number of steps left
    seemed like large values

    #make the problem file and store in the sayphi / gripper folder where the lisp program is
    # get the state and recover the encoding like you did for training the NN

    then get the value for this node.

    pass


class GPfeaturesHeuristic(Heuristic): #class name must end with "Heuristic"
    def __init__(self, task):
        self.task = task


    def __call__(self, node):
        """ Returns the heuristic value for "node". """
        h = compute_NN_wGPF_heuristic(node.state)
        h = 1.0
        #For nodes that are known to be deadends (i.e. there is no valid plan that
        # reaches the goal from this node), a heuristic value of `float('inf')` should
        # be returned.
        return h
