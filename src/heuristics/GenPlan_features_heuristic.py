#
# Heuristic using features generated for generalized planning
#

"""
Landmarks Heuristic
"""

from collections import defaultdict
import copy

from heuristics.heuristic_base import Heuristic


def compute_NN_wGPF_heuristic(task):
    pass


class GP_features_Heuristic(Heuristic): #class name must end with "Heuristic"
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

NEXT USE THIS DUMMY HEURISTIC AND RUN THE CODE