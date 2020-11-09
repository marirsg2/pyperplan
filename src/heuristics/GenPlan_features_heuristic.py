#
# Heuristic using features generated for generalized planning
#

"""
Landmarks Heuristic
"""

import torch
import os
import csv
import numpy as np
from heuristics.GenPlan_HeuristicSupport.PDDL_util_func import *
from heuristics.heuristic_base import Heuristic
from heuristics.GenPlan_HeuristicSupport.Gripper_GPfeatures_NN import \
        domain_name, trained_model_location, lisp_input_file,lisp_feature_gen_base_folder,\
        relative_location_problem_and_feature_files

# The following line is because the cwd from which this file is called is the src directory
trained_model_location = "./heuristics/GenPlan_HeuristicSupport/" + trained_model_location

def compute_NN_wGPF_heuristic(state_frozen_set_proposition_strings,goal_frozen_set_proposition_strings):
    cwd = os.getcwd()
    #unpickle the saved model, and do inference
    #todo NOTE oddly you have to import the NN class from the "__main__" call in the pyperplan.py script else it complains that it could
    # not find the NN class even if you import it here. strange.
    nn_model = torch.load(trained_model_location)
    nn_model.eval()
    #todo we repeat the model loading too often, load and save in the heuristics class !!
    #make the problem file and store in the sayphi / gripper folder where the lisp program is
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
    data_input = torch.tensor([state_features],dtype=torch.float)
    distance = nn_model.forward(data_input)
    return float(distance.data[0][0])





class GPfeaturesHeuristic(Heuristic): #class name must end with "Heuristic"
    def __init__(self, task):
        self.task = task


    def __call__(self, node):
        """ Returns the heuristic value for "node". """
        h = compute_NN_wGPF_heuristic(node.state,self.task.goals)
        #For nodes that are known to be deadends (i.e. there is no valid plan that
        # reaches the goal from this node), a heuristic value of `float('inf')` should
        # be returned.
        return h
