#
# Heuristic using features generated for generalized planning
#

"""
Landmarks Heuristic
"""

import torch
import os
import csv
import pickle
import numpy as np
import socket
from heuristics.GenPlan_HeuristicSupport.PDDL_util_func import *
from heuristics.heuristic_base import Heuristic
from heuristics.GenPlan_HeuristicSupport.Gripper_GPfeatures_NN_w_SOCKET import \
        domain_name, trained_model_location, lisp_input_file,lisp_feature_gen_base_folder,\
        relative_location_problem_and_feature_files,preprocessed_data_save_file

# The following line is because the cwd from which this file is called is the src directory
trained_model_location = "./heuristics/GenPlan_HeuristicSupport/" + trained_model_location
preprocessed_data_save_file = "./heuristics/GenPlan_HeuristicSupport/" + preprocessed_data_save_file

RF_model_file_name = "../benchmarks/gripper_MOD/RF_gripper.p"


def SOCKET_compute_RF_wGPF_heuristic(state_frozen_set_proposition_strings, goal_frozen_set_proposition_strings, lisp_socket):
    cwd = os.getcwd()
    #unpickle the saved model, and do inference
    #todo NOTE oddly you have to import the NN class from the "__main__" call in the pyperplan.py script else it complains that it could
    # not find the NN class even if you import it here. strange.
    with open(RF_model_file_name,"rb") as src:
        rf_model = pickle.load(src)

    #get the normalization information
    with open(preprocessed_data_save_file,'rb') as src:
        _ = pickle.load(src)
        input_mean = pickle.load(src)
        input_std = pickle.load(src)
        output_mean = pickle.load( src)
        output_std = pickle.load( src)

    #todo we repeat the model loading too often, load and save in the heuristics class !!
    #next here we make the problem file and store in the sayphi / gripper folder where the lisp program is
    # get the state and recover the encoding like you did for training the NN
    convert_searchNode_to_gripper_problem_file(state_frozen_set_proposition_strings, goal_frozen_set_proposition_strings, lisp_input_file)
    #convert the input file into one long string for socket communication with the lisp code
    with open(lisp_input_file,"r") as src:
        all_lines = src.readlines()
        problem_file_desc = " ".join([x.replace("\n","") for x in all_lines]) +"\n" #the last new line is to end the descriptor

    #now use the socket comm
    print('Sending problem = ',problem_file_desc)
    lisp_socket.send(bytes(problem_file_desc,"utf-8"))
    print('  Problem sent')
    print('  Receiving new generalized state')
    msg = lisp_socket.recv(100000).decode("utf-8")
    while not msg.endswith("-1"):  # yup thats a lousy end char, but so it is
        msg += lisp_socket.recv(100000).decode("utf-8")
    print('  Received', msg)
    state_features = [ int(x) for x in msg.replace('\"',"").replace(" ","").split(",") ][:-1] #ignore the last -1 which is an eof

    #----old code
    # # copy this file to the target location for lisp feat gen to read
    # os.system("cp " + lisp_input_file + " " + lisp_feature_gen_base_folder + "/" + relative_location_problem_and_feature_files)
    # # now call the lisp program to get the features, and save <features,distance>
    # os.chdir(lisp_feature_gen_base_folder)
    # os.system(lisp_feature_gen_base_folder + "/run-deepplan.sh " + domain_name + " " + lisp_input_file)
    # os.chdir(cwd)
    # now read the csv file containing the state description and convert to vector format and save
    # in "preprocessed_data"
    # result_features_loc = lisp_feature_gen_base_folder + "/" +relative_location_problem_and_feature_files + "/state-deepplan.csv"
    # state_features = []
    # with open(result_features_loc, newline='') as csvfile:
    #     feature_reader = csv.reader(csvfile, delimiter=',', quotechar='\'')
    #     state_features = [int(x) for x in feature_reader.__next__()]
    #-----old code


    data_input = np.array([state_features])
    distance = rf_model.predict(data_input)[0]*output_std + output_mean
    return int(distance) + 1 #rounding up



# def SOCKET_compute_NN_wGPF_heuristic(state_frozen_set_proposition_strings, goal_frozen_set_proposition_strings, lisp_socket):
#     cwd = os.getcwd()
#     #unpickle the saved model, and do inference
#     #todo NOTE oddly you have to import the NN class from the "__main__" call in the pyperplan.py script else it complains that it could
#     # not find the NN class even if you import it here. strange.
#     nn_model = torch.load(trained_model_location)
#     nn_model.eval()
#     #get the normalization information
#     with open(preprocessed_data_save_file,'rb') as src:
#         _ = pickle.load(src)
#         input_mean = pickle.load(src)
#         input_std = pickle.load(src)
#         output_mean = pickle.load( src)
#         output_std = pickle.load( src)
#
#     #todo we repeat the model loading too often, load and save in the heuristics class !!
#     #next here we make the problem file and store in the sayphi / gripper folder where the lisp program is
#     # get the state and recover the encoding like you did for training the NN
#     convert_searchNode_to_gripper_problem_file(state_frozen_set_proposition_strings, goal_frozen_set_proposition_strings, lisp_input_file)
#     #convert the input file into one long string for socket communication with the lisp code
#     with open(lisp_input_file,"r") as src:
#         all_lines = src.readlines()
#         problem_file_desc = " ".join([x.replace("\n","") for x in all_lines]) +"\n" #the last new line is to end the descriptor
#
#     #now use the socket comm
#     print('Sending problem = ',problem_file_desc)
#     lisp_socket.send(bytes(problem_file_desc,"utf-8"))
#     print('  Problem sent')
#     print('  Receiving new generalized state')
#     msg = lisp_socket.recv(100000).decode("utf-8")
#     while not msg.endswith("-1"):  # yup thats a lousy end char, but so it is
#         msg += lisp_socket.recv(100000).decode("utf-8")
#     print('  Received', msg)
#     state_features = [ int(x) for x in msg.replace('\"',"").replace(" ","").split(",") ][:-1] #ignore the last -1 which is an eof
#
#     #----old code
#     # # copy this file to the target location for lisp feat gen to read
#     # os.system("cp " + lisp_input_file + " " + lisp_feature_gen_base_folder + "/" + relative_location_problem_and_feature_files)
#     # # now call the lisp program to get the features, and save <features,distance>
#     # os.chdir(lisp_feature_gen_base_folder)
#     # os.system(lisp_feature_gen_base_folder + "/run-deepplan.sh " + domain_name + " " + lisp_input_file)
#     # os.chdir(cwd)
#     # now read the csv file containing the state description and convert to vector format and save
#     # in "preprocessed_data"
#     # result_features_loc = lisp_feature_gen_base_folder + "/" +relative_location_problem_and_feature_files + "/state-deepplan.csv"
#     # state_features = []
#     # with open(result_features_loc, newline='') as csvfile:
#     #     feature_reader = csv.reader(csvfile, delimiter=',', quotechar='\'')
#     #     state_features = [int(x) for x in feature_reader.__next__()]
#     #-----old code
#
#     data_input = (torch.tensor([state_features],dtype=torch.float)-input_mean)/input_std
#     distance = nn_model.forward(data_input).data[0][0]*output_std + output_mean
#     return int(distance) + 1 #rounding up


def compute_NN_wGPF_heuristic(state_frozen_set_proposition_strings,goal_frozen_set_proposition_strings):
    cwd = os.getcwd()
    #unpickle the saved model, and do inference
    #todo NOTE oddly you have to import the NN class from the "__main__" call in the pyperplan.py script else it complains that it could
    # not find the NN class even if you import it here. strange.
    nn_model = torch.load(trained_model_location)
    nn_model.eval()
    #get the normalization information
    with open(preprocessed_data_save_file,'rb') as src:
        _ = pickle.load(src)
        input_mean = pickle.load(src)
        input_std = pickle.load(src)
        output_mean = pickle.load( src)
        output_std = pickle.load( src)

    #todo we repeat the model loading too often, load and save in the heuristics class !!
    #next here we make the problem file and store in the sayphi / gripper folder where the lisp program is
    # get the state and recover the encoding like you did for training the NN
    convert_searchNode_to_gripper_problem_file(state_frozen_set_proposition_strings, goal_frozen_set_proposition_strings, lisp_input_file)
    # copy this file to the target location for lisp feat gen to read
    os.system("cp " + lisp_input_file + " " + lisp_feature_gen_base_folder + "/" + relative_location_problem_and_feature_files)
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
    data_input = (torch.tensor([state_features],dtype=torch.float)-input_mean)/input_std
    distance = nn_model.forward(data_input).data[0][0]*output_std + output_mean
    return int(distance) + 1 #rounding up





class GPfeaturesHeuristic(Heuristic): #class name must end with "Heuristic"
    def __init__(self, task):
        self.task = task

    def set_socket(self,lisp_socket):
        self.lisp_socket = lisp_socket


    def __call__(self, node):
        global clientsocket
        """ Returns the heuristic value for "node". """
        h = SOCKET_compute_RF_wGPF_heuristic(node.state, self.task.goals, self.lisp_socket)
        #For nodes that are known to be deadends (i.e. there is no valid plan that
        # reaches the goal from this node), a heuristic value of `float('inf')` should
        # be returned.
        return h
