import math
import torch
import torch.nn as nn
import torch.nn.functional as F

"""

The features will be numeric and binary. So the input vector should be an int form.
The training will be to predict the number of actions left from the goal.
Training data would be a set of traces that is a sequence of states (full states, and not actions), and the goal.  
We preprocess this training data into vector of general features, and the target is the number of actions left to the goal. 

The inference process would be the heuristic fed to the pyperplan
"""

#TODO !! suggest policy nx variant to Daniel and Vamsi. output = Probability of correct action. mimics the asnets, albeit one action at a time.