import os
import csv
import socket
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
EPSILON = 1e-20
NUM_EPOCHS = 50
BATCH_SIZE = 32
BATCH_LOG_INTERVAL = 100
HIDDEN_DIM_SIZE = 500
LEARNING_RATE = 1E-3
domain_name = "blocksworld" #fixed set of domains
home_dir = "/home/yochan-ubuntu19"
lisp_feature_gen_base_folder = home_dir +"/workspace/deepplan/dist"
relative_location_problem_and_feature_files = "planning/sayphi/domains/blocksworld/probsets"
target_domain_name = "blocksworld" #should match folder name in the lisp program directory
lisp_input_file = lisp_feature_gen_base_folder + "/" +relative_location_problem_and_feature_files +"/test.pddl"
train_data_file = "../GenPlan_data/JPMC_GenPlan_Blocksworld.p"
preprocessed_data_save_file = train_data_file.replace(".p", "_preprocessed.p")
# pickled_preprocessed_data = None # None # or its the save file preprocessed_data_save_file
pickled_preprocessed_data = preprocessed_data_save_file # None #or its the save file preprocessed_data_save_file
trained_model_location = "blocksworld_GP_NN_heuristic_weights_multi_setting.pt"



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
        # print(x)
        h_relu = F.relu(self.linear1(x))
        # print(self.linear1(x))
        # print("===================")
        # print(h_relu)
        h_relu = F.relu(self.linear2(h_relu))
        h_relu = F.relu(self.linear3(h_relu))
        y_pred = F.relu(self.linear4(h_relu))
        return y_pred
    #end def forward


def train_NN(train_torch_dataset, num_GP_features =100, hidden_dim_size = 50):
    NN_model = GP_NN_heuristic_model_class(num_GP_features, hidden_dim_size)
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.SGD(NN_model.parameters(), lr=LEARNING_RATE)
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
    if pickled_preprocessed_data == None:  # then we need to generate the dataset
        print('Starting')
        print("********DOUBLE CHECK THE DOMAIN, ARE YOU USING THE RIGHT DOMAIN !!********")
        print("IMPORTANT make sure you executed ./run-deepplan.sh blocksworld test.pddl")
        print("REMEMBER TO START CLIENT FIRST, else you may have to restart terminal running deeplan.sh or computer")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # "127.0.0.1"
        s.bind(('localhost', 1800))
        s.listen(1)
        print('  Waiting for client')
        lisp_socket, address = s.accept()
        print(f"  Connection from {address} has been established.")
        print('  Sending OK')
        lisp_socket.send(bytes("ok\n", "utf-8"))
        print('  Sent OK')
        print("IMPORTANT make sure you executed ./run-deepplan.sh blocksworld test.pddl")
        #========================
        # now use the socket comm


        #========================

        preprocessed_torch_dataset = []
        feature_size = -1

        raw_data = None
        with open(train_data_file,"rb") as src:
            raw_data = pickle.load(src)

        #todo call the init function for the domain in question
        # note if you do this, you can replace the features.lisp file, so maybe NOT do it, if you have a new feature set
        # cwd = os.getcwd()
        # os.chdir(lisp_feature_gen_base_folder)
        # os.system("./init-deepplan.sh " + domain_name) #cannot execute script from different directory as code tries to access deeplan.mem from local offset
        # os.chdir(cwd)

        #get the feature size --this is ugly but prevents repetitive checks or reassignments to feature size
        state, goal, distance = list(raw_data)[1]
        # prepare to call the lisp program to get the features
        convert_to_blocksworld_problem_file(state, goal, lisp_input_file)
        with open(lisp_input_file, "r") as src:
            all_lines = src.readlines()
            problem_file_desc = " ".join(
                [x.replace("\n", "") for x in all_lines]) + "\n"  # the last new line is to end the descriptor
        #---end with
        # print('Sending problem = ', problem_file_desc)
        lisp_socket.send(bytes(problem_file_desc, "utf-8"))
        print('  Problem sent')
        print('  Receiving new generalized state')
        msg = lisp_socket.recv(100000).decode("utf-8")
        while not msg.endswith("-1"):  # yup thats our end char, so it is
            msg += lisp_socket.recv(100000).decode("utf-8")
        print('  Received', msg)
        state_features = [int(x) for x in msg.replace('\"', "").replace(" ", "").split(",")][:-1] #ignore the last "-1"
        feature_size = len(state_features)
        # OLD VERSION #copy this file to the target location for lisp feat gen to read
        # os.system("cp " + lisp_input_file + " " + lisp_feature_gen_base_folder + "/" + relative_location_problem_and_feature_files)
        # # now call the lisp program to get the features, and save <features,distance>
        # os.chdir(lisp_feature_gen_base_folder)
        # os.system(lisp_feature_gen_base_folder + "/run-deepplan.sh "+domain_name + " " + lisp_input_file)
        # os.chdir(cwd)
        # result_features_loc = lisp_feature_gen_base_folder + "/" + relative_location_problem_and_feature_files + "/state-deepplan.csv"
        # state_features = []
        # with open(result_features_loc, newline='') as csvfile:
        #     feature_reader = csv.reader(csvfile, delimiter=',', quotechar='\'')
        #     feature_size = len(feature_reader.__next__())
        #------end old version
        # get the feature size
        preprocessed_data_input = []
        preprocessed_data_output = []
        curr_state_feat = np.zeros(feature_size)
        prev_state_feat = np.zeros(feature_size)
        max_distance = 0.0
        distance_dict = {}
        print("feature_size = ",feature_size)
        shuffle(raw_data)
        for state,goal,distance in raw_data:
            # print("ENSURE YOU HAVE REMOVED THE size LIMITATION ON THE RAW DATA ")
            # print("ENSURE YOU HAVE REMOVED THE size  LIMITATION ON THE RAW DATA ")
            # print("ENSURE YOU HAVE REMOVED THE size  LIMITATION ON THE RAW DATA ")
            if distance > max_distance:
                print("new max distance =", distance)
                max_distance = distance
            try:
                distance_dict[distance] += 1
            except KeyError:
                distance_dict[distance] = 1

            # distance = 5 #todo remove this, purely for testing
            convert_to_blocksworld_problem_file(state, goal, lisp_input_file)
            with open(lisp_input_file, "r") as src:
                all_lines = src.readlines()
                problem_file_desc = " ".join(
                    [x.replace("\n", "") for x in all_lines]) + "\n"  # the last new line is to end the descriptor
            # ---end with
            # print('Sending problem = ', problem_file_desc)
            lisp_socket.send(bytes(problem_file_desc, "utf-8"))
            print('  Problem sent')
            print('  Receiving new generalized state')
            msg = lisp_socket.recv(100000).decode("utf-8")
            while not msg.endswith("-1"):  # yup thats a lousy end char, but so it is
                msg += lisp_socket.recv(100000).decode("utf-8")
            print('  Received', msg)
            state_features = [int(x) for x in msg.replace('\"', "").replace(" ", "").split(",")][:-1] #ignore the last "-1"
            curr_state_feat = np.array(state_features)
            diff = curr_state_feat - prev_state_feat
            print(np.sum(diff))
            prev_state_feat = curr_state_feat
            #todo save as torch dataset, better for loading and shuffling
            preprocessed_data_input.append(state_features)
            preprocessed_data_output.append([distance])#yes it needs to be a nested list/array
            #end with
        #end for
        print("distance dict = ", distance_dict)
        data_input = torch.tensor(preprocessed_data_input,dtype=torch.float)
        input_mean = torch.mean(data_input,0)
        input_std = torch.std(data_input,0)+EPSILON
        data_input = (data_input-input_mean)/input_std
        # input_max = torch.max(data_input,0)[0]
        # input_min = torch.min(data_input,0)[0]
        data_output = torch.tensor(preprocessed_data_output,dtype=torch.float)
        # output_mean = torch.mean(data_output)
        # output_std = torch.std(data_output)
        # data_output = (data_output - output_mean) / output_std
        output_mean = 0.0 # we prefer keeping the original distance values, scaling hurts the heuristic computation
        output_std = 1
        preprocessed_torch_dataset = TensorDataset(data_input,data_output)

        #--now we have the training data in the right format, save with the mean and std dev for later inference
        with open(preprocessed_data_save_file, "wb") as dest:
            pickle.dump(preprocessed_torch_dataset, dest)
            pickle.dump(input_mean,dest)
            pickle.dump(input_std,dest)
            pickle.dump(output_mean, dest)
            pickle.dump(output_std, dest)
        print("finished preprocessing data")
    else: #if pickled_preprocessed_data != None:
        with open(preprocessed_data_save_file, "rb") as src:
            preprocessed_torch_dataset = pickle.load(src)
            feature_size = preprocessed_torch_dataset[0][0].shape[0]

    #end else - for preparing the preprocessed data
    print("num train data = ", preprocessed_torch_dataset.tensors[1].shape)

    #todo get dim size based on lisp program feedback, set as feature size
    trained_NN_model = train_NN(preprocessed_torch_dataset, num_GP_features = feature_size, hidden_dim_size = HIDDEN_DIM_SIZE)
    #---now save the NN
    torch.save(trained_NN_model,trained_model_location)
    loaded_model  = torch.load(trained_model_location)
    print(loaded_model)
    print("num train data = ", preprocessed_torch_dataset.tensors[1].shape)