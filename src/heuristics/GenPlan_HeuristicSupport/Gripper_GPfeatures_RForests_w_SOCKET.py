import os
import csv
from sklearn.ensemble import GradientBoostingRegressor
import socket
import math
import random
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
NUM_EPOCHS = 20
BATCH_SIZE = 32
BATCH_LOG_INTERVAL = 100
HIDDEN_DIM_SIZE = 2000
LEARNING_RATE = 3E-5
domain_name = "gripper" #fixed set of domains
home_dir = "/home/yochan-ubuntu19"
lisp_feature_gen_base_folder = home_dir +"/workspace/deepplan/dist"
relative_location_problem_and_feature_files = "planning/sayphi/domains/gripper/probsets"
target_domain_name = "gripper" #should match folder name in the lisp program directory
lisp_input_file = "./test.pddl"
train_data_file = "../GenPlan_data/JPMC_GenPlan_gripper_singleSetting_varyRoomsBalls_40k.p"
preprocessed_data_save_file = train_data_file.replace(".p", "_preprocessed_8008.p")
pickled_preprocessed_data = None # None # or its the save file preprocessed_data_save_file
# pickled_preprocessed_data = preprocessed_data_save_file # None #or its the save file preprocessed_data_save_file
RF_model_file_name = "RF_gripper.p"



def train_RF(X_train,y_train):
    reg = GradientBoostingRegressor(random_state=0)
    reg.fit(X_train, y_train)
    # print(reg.score(X_train,y_train))
    print((np.linalg.norm(y_train-reg.predict(X_train))**2/len(y_train)))
    # print(math.sqrt(np.linalg.norm(y_train-reg.predict(X_train))**2/len(y_train)))
    return reg




if __name__ == "__main__":
    if pickled_preprocessed_data == None: #then we need to generate the dataset
        print('Starting')
        print("********DOUBLE CHECK THE DOMAIN, ARE YOU USING THE RIGHT DOMAIN !!********")
        print("IMPORTANT make sure you executed ./run-deepplan.sh gripper test.pddl")
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
        print("IMPORTANT make sure you executed /run-deepplan.sh gripper test.pddl ")
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
        convert_to_gripper_problem_file(state, goal, lisp_input_file)
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
        random.seed(3)
        shuffle(raw_data)
        for raw_data_idx in range(len(raw_data)):
            state,goal,distance = raw_data[raw_data_idx]
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
            convert_to_gripper_problem_file(state, goal, lisp_input_file)
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

            if (raw_data_idx+1) % 1000 == 0:
                print("saved data of size = ",raw_data_idx+1)
                data_input = torch.tensor(preprocessed_data_input, dtype=torch.float)
                input_mean = torch.mean(data_input, 0)
                input_std = torch.std(data_input, 0) + EPSILON
                data_input = (data_input - input_mean) / input_std
                print("printout of 10 data points")
                for i in range(1, 10):
                    " ".join([str(x) for x in preprocessed_data_input[i]])
                data_output = torch.tensor(preprocessed_data_output, dtype=torch.float)
                output_mean = 0.0  # we prefer keeping the original distance values, scaling hurts the heuristic computation
                output_std = 1
                preprocessed_torch_dataset = TensorDataset(data_input, data_output)
                # --now we have the training data in the right format, save with the mean and std dev for later inference
                with open(preprocessed_data_save_file, "wb") as dest:
                    pickle.dump(preprocessed_torch_dataset, dest)
                    pickle.dump(input_mean, dest)
                    pickle.dump(input_std, dest)
                    pickle.dump(output_mean, dest)
                    pickle.dump(output_std, dest)
                #---end with
                train_loader = DataLoader(preprocessed_torch_dataset, batch_size=len(preprocessed_torch_dataset))
                X_data = next(iter(train_loader))[0].numpy()
                train_loader = DataLoader(preprocessed_torch_dataset, batch_size=len(preprocessed_torch_dataset))
                y_data = next(iter(train_loader))[1].numpy()
                y_data = y_data.ravel()
                trained_RF_model = train_RF(X_data, y_data)
                with open(RF_model_file_name, "wb") as dest:
                    pickle.dump(trained_RF_model, dest)


        #end for
        print("distance dict = ", distance_dict)
        data_input = torch.tensor(preprocessed_data_input,dtype=torch.float)
        input_mean = torch.mean(data_input,0)
        input_std = torch.std(data_input,0)+EPSILON
        data_input = (data_input-input_mean)/input_std
        print("printout of 10 data points")
        for i in range(1,10):
            " ".join([str(x) for x in preprocessed_data_input[i]])
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

    #end if pickled_preprocessed_data == None:
    elif pickled_preprocessed_data != None:
        with open(preprocessed_data_save_file, "rb") as src:
            preprocessed_torch_dataset = pickle.load(src)
            feature_size = preprocessed_torch_dataset[0][0].shape[0]
    print("num train data = ", preprocessed_torch_dataset.tensors[1].shape)

    #todo get dim size based on lisp program feedback, set as feature size
    train_loader = DataLoader(preprocessed_torch_dataset, batch_size=len(preprocessed_torch_dataset))
    X_data = next(iter(train_loader))[0].numpy()
    train_loader = DataLoader(preprocessed_torch_dataset, batch_size=len(preprocessed_torch_dataset))
    y_data = next(iter(train_loader))[1].numpy()
    y_data = y_data.ravel()
    trained_RF_model = train_RF(X_data,y_data)
    #---now save the NN

    with open(RF_model_file_name,"wb") as dest:
        pickle.dump(trained_RF_model,dest)

