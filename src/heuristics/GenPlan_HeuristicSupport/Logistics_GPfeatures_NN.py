import os
import csv
import math
import numpy as np
import torch
import torch.nn.functional as F
import pickle
from random import shuffle
from torch.utils.data import TensorDataset, DataLoader
from heuristics.GenPlan_HeuristicSupport.PDDL_util_func import *
"""

The features will be numeric and binary. So the input vector should be an int form.
The training will be to predict the number of actions left from the goal.
Training data would be a set of traces that is a sequence of states (full states, and not actions), and the goal.  
We preprocess this training data into vector of general features, and the target is the number of actions left to the goal. 

The inference process would be the heuristic fed to the pyperplan
"""

NUM_EPOCHS = 1000
BATCH_SIZE = 32
BATCH_LOG_INTERVAL = 10
HIDDEN_DIM_SIZE = 500
domain_name = "logistics" #fixed set of domains
home_dir = "/home/yochan-ubuntu19"
lisp_feature_gen_base_folder = home_dir +"/workspace/deepplan/dist"
relative_location_problem_and_feature_files = "planning/sayphi/domains/logistics/probsets"
target_domain_name = "logistics" #should match folder name in the lisp program directory
lisp_input_file = "./test.pddl"
train_data_file = "../GenPlan_data/JPMC_GenPlan_logistics_multiSetting.p"
preprocessed_data_save_file = train_data_file.replace(".p", "_preprocessed.p")
pickled_preprocessed_data = None # or its the save file preprocessed_data_save_file
# pickled_preprocessed_data = preprocessed_data_save_file # None #or its the save file preprocessed_data_save_file
trained_model_location = "GP_NN_heuristic_weights.pt"


#TODO !! suggest policy nx variant to Daniel and Vamsi. output = Probability of correct action. mimics the asnets, albeit one action at a time.

class GP_NN_heuristic_model_class(torch.nn.Module):
    def __init__(self, num_GP_features, L1_dim_size):
        """
        In the constructor we instantiate two nn.Linear modules and assign them as
        member variables.
        """
        super(GP_NN_heuristic_model_class, self).__init__()
        self.linear1 = torch.nn.Linear(num_GP_features, L1_dim_size)
        self.linear2 = torch.nn.Linear(L1_dim_size, int(L1_dim_size / 2))
        self.linear3 = torch.nn.Linear(int(L1_dim_size / 2), int(L1_dim_size / 4))
        self.linear4 = torch.nn.Linear(int(L1_dim_size / 4), 1)

    def forward(self, x):
        """
        In the forward function we accept a Tensor of input data and we must return
        a Tensor of output data. We can use Modules defined in the constructor as
        well as arbitrary operators on Tensors.
        """
        h_relu = F.relu(self.linear1(x))
        h_relu = F.relu(self.linear2(h_relu))
        h_relu = F.relu(self.linear3(h_relu))
        y_pred = F.relu(self.linear4(h_relu))
        return y_pred
    #end def forward


def train_NN(train_torch_dataset, num_GP_features =100, hidden_dim_size = 50):
    NN_model = GP_NN_heuristic_model_class(num_GP_features, hidden_dim_size)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(NN_model.parameters(), lr=0.0001)
    optimizer.zero_grad()
    params = {'batch_size': BATCH_SIZE,
              'shuffle': True,
              'num_workers': 4}
    data_loader = DataLoader(train_torch_dataset,**params)
    for epoch in range(NUM_EPOCHS):
        for batch_idx,(batch_input, batch_output) in enumerate(data_loader):
            optimizer.zero_grad()
            batch_pred = NN_model(batch_input)
            loss = criterion(batch_pred, batch_output)
            loss.backward()  # accumulate gradients
            optimizer.step()
            if batch_idx%BATCH_LOG_INTERVAL == 0 :
                print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}'.format(
                    epoch, batch_idx * BATCH_SIZE, len(data_loader.dataset),
                           100. * batch_idx / len(data_loader), loss.item()))
            if batch_idx == 0 and epoch%10 == 0:
                print(batch_pred)
                print(batch_output)
        #end for loop through batches
    #end for loop through epochs

    return NN_model
#end def train_NN


if __name__ == "__main__":
    preprocessed_torch_dataset = []
    feature_size = -1
    if pickled_preprocessed_data != None:
        with open(preprocessed_data_save_file, "rb") as src:
            preprocessed_torch_dataset = pickle.load(src)
            feature_size = preprocessed_torch_dataset[0][0].shape[0]
    else:
        raw_data = None
        with open(train_data_file,"rb") as src:
            raw_data = pickle.load(src)

        #todo call the init function for the domain in question
        cwd = os.getcwd()
        os.chdir(lisp_feature_gen_base_folder)
        os.system("./init-deepplan.sh " + domain_name) #cannot execute script from different directory as code tries to access deeplan.mem from local offset
        os.chdir(cwd)

        #get the feature size --this is ugly but prevents repetitive checks or reassignments to feature size
        state, goal, distance = raw_data[1]
        # prepare to call the lisp program to get the features
        convert_to_logistics_problem_file(state, goal, lisp_input_file)
        #copy this file to the target location for lisp feat gen to read
        os.system("cp " + lisp_input_file + " " + lisp_feature_gen_base_folder + "/" + relative_location_problem_and_feature_files)
        # now call the lisp program to get the features, and save <features,distance>
        os.chdir(lisp_feature_gen_base_folder)
        os.system(lisp_feature_gen_base_folder + "/run-deepplan.sh "+domain_name + " " + lisp_input_file)
        os.chdir(cwd)
        # get the feature size
        result_features_loc = lisp_feature_gen_base_folder + "/" + relative_location_problem_and_feature_files + "/state-deepplan.csv"
        state_features = []
        with open(result_features_loc, newline='') as csvfile:
            feature_reader = csv.reader(csvfile, delimiter=',', quotechar='\'')
            feature_size = len(feature_reader.__next__())

        preprocessed_data_input = []
        preprocessed_data_output = []
        curr_state_feat = np.zeros(feature_size)
        prev_state_feat = np.zeros(feature_size)
        for state,goal,distance in raw_data:
            convert_to_logistics_problem_file(state,goal,lisp_input_file)
            os.system("cp "+lisp_input_file + " " + lisp_feature_gen_base_folder + "/" +relative_location_problem_and_feature_files)
            # now call the lisp program to get the features, and save <features,distance>
            os.chdir(lisp_feature_gen_base_folder)
            os.system(lisp_feature_gen_base_folder + "/run-deepplan.sh " + domain_name + " " + lisp_input_file)
            os.chdir(cwd)
            # now read the csv file containing the state description and convert to vector format and save
            # in "preprocessed_data"
            result_features_loc = lisp_feature_gen_base_folder + "/" +relative_location_problem_and_feature_files + "/state-deepplan.csv"
            state_features = []
            with open(result_features_loc, newline='') as csvfile:
                feature_reader = csv.reader(csvfile, delimiter=',', quotechar='\'')
                state_features = [int(x) for x in feature_reader.__next__()]
                curr_state_feat = np.array(state_features)
                diff = curr_state_feat - prev_state_feat
                print(np.sum(diff))
                prev_state_feat = curr_state_feat

                #todo save as torch dataset, better for loading and shuffling
                preprocessed_data_input.append(state_features)
                preprocessed_data_output.append([distance])#yes it needs to be a nested list/array
            #end with
        #end for
        data_input = torch.tensor(preprocessed_data_input,dtype=torch.float)
        data_output = torch.tensor(preprocessed_data_output,dtype=torch.float)
        preprocessed_torch_dataset = TensorDataset(data_input,data_output)


        #--now we have the training data in the right format
        with open(preprocessed_data_save_file, "wb") as dest:
            pickle.dump(preprocessed_torch_dataset, dest)
        print("finished preprocessing data")

    #end else - for preparing the preprocessed data

    #todo get dim size based on lisp program feedback, set as feature size
    trained_NN_model = train_NN(preprocessed_torch_dataset, num_GP_features = feature_size, hidden_dim_size = HIDDEN_DIM_SIZE)
    #---now save the NN
    torch.save(trained_NN_model,trained_model_location)