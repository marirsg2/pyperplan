import os
import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import pickle
from heuristics.GenPlan_HeuristicSupport.PDDL_util_func import *
"""

The features will be numeric and binary. So the input vector should be an int form.
The training will be to predict the number of actions left from the goal.
Training data would be a set of traces that is a sequence of states (full states, and not actions), and the goal.  
We preprocess this training data into vector of general features, and the target is the number of actions left to the goal. 

The inference process would be the heuristic fed to the pyperplan
"""

NUM_EPOCHS = 100
HIDDEN_DIM_SIZE = 50
lisp_feature_gen_base_folder = "~/workspace/deepplan/dist"
relative_location_gen_features_file = "planning/sayphi/domains/logistics"
lisp_input_file = "./state_and_goal.txt"
train_data_file = "../GenPlan_data/JPMC_GenPlan_logistics_multiSetting.p"
trained_model_location = "GP_NN_heuristic_weights.pt"
domain_name = "logistics" #fixed set of domains


#TODO !! suggest policy nx variant to Daniel and Vamsi. output = Probability of correct action. mimics the asnets, albeit one action at a time.

class GP_NN_heuristic_model_class(torch.nn.Module):
    def __init__(self, num_GP_features, H):
        """
        In the constructor we instantiate two nn.Linear modules and assign them as
        member variables.
        """
        super(GP_NN_heuristic_model_class, self).__init__()
        self.linear1 = torch.nn.Linear(num_GP_features, H)
        self.linear2 = torch.nn.Linear(H, 1)

    def forward(self, x):
        """
        In the forward function we accept a Tensor of input data and we must return
        a Tensor of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Tensors.
        """
        h_relu = F.relu(self.linear1(x))
        y_pred = F.relu(self.linear2(h_relu))
        return y_pred


def train_NN(train_data, num_GP_features =100, hidden_dim_size = 50):
    NN_model = GP_NN_heuristic_model_class(num_GP_features, hidden_dim_size)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(NN_model.parameters(), lr=1e-4)
    for t in range(NUM_EPOCHS):
        for state, distance_to_goal in train_data:
            x = [1.0]*num_GP_features#todo call Daniels lisp code through another process. Or execute his program through an os interface (easiest)
            y_pred = NN_model(x)
            y = distance_to_goal
            loss = criterion(y_pred, y)
            if t % 100 == 99:
                print(t, loss.item())
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    #end for
    return NN_model
#end def train_NN


if __name__ == "__main__":
    train_data = None
    with open(train_data_file,"rb") as src:
        train_data = pickle.load(src)
    # for x in train_data:
    #     print(x)
    #CONVERT INTO FILE. pass to lisp program

    feature_size = -1
    #get the feature size
    state, goal, distance = train_data[1]
    # prepare to call the lisp program to get the features
    convert_to_logistics_problem_file(state, goal, lisp_input_file)
    # now call the lisp program to get the features, and save <features,distance>
    # note we assume the init command has been called for the domain in question
    os.system()
    # now read the csv file containing the state description and determine the feature size
    feature_size = -1
    preprocessed_data = []
    for state,goal,distance in train_data:
        #prepare to call the lisp program to get the features
        convert_to_logistics_problem_file(state,goal,lisp_input_file)
        #now call the lisp program to get the features, and save <features,distance>
        #note we assume the init command has been called for the domain in question
        os.system()
        #now read the csv file containing the state description and convert to vector format and save
        # in preprocessed data


    #end for loop through the train data
    #todo get dim size based on lisp program feedback, set as feature size
    trained_NN_model = train_NN(train_data , num_GP_features = 100 , hidden_dim_size = HIDDEN_DIM_SIZE)

    #---now train the NN and save it
    torch.save(trained_NN_model,trained_model_location)