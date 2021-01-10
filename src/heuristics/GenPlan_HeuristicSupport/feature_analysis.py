"""
this reads the training data for the neural network, and decides what features have changed and what have not changed. This
can be used to give feedback to the lisp code as to what features to generate
v0) just binary check on what changes and what doesnt change, remove static features
v1) remove redundant features/ heavily correlated features. covariance matrix can help for this.
    also looking at the correlation with the output might help, but not obvious, 
    perhaps seemingly uncorrelated features (individually)
    when combined may produce a good feature.
"""
import pickle
import torch
import numpy as np
import pandas as pd


EPSILON = 1e-20 #zero is actually 1e-20. This was to avoid div by zero error.
train_data_file = "../GenPlan_data/JPMC_GenPlan_gripper_singleSetting_varyRoomsBalls_40k.p"
preprocessed_data_loc = train_data_file.replace(".p", "_preprocessed.p")
bad_feat_storage_file = "./gripper_no_change_feat_indexes.csv"
with open(preprocessed_data_loc,"rb") as src:
    torch_dataset = pickle.load(src)
    input_mean = pickle.load(src)
    input_std = pickle.load(src)
    output_mean = pickle.load(src)
    output_std = pickle.load(src)

#todo use the input std dev to determine if the feature changes. if 0, then note that feature index to be removed

input_std = input_std.detach().numpy()
bad_feature_idx = np.array(np.where(input_std == EPSILON)[0],dtype=int)
print("len(bad_feature_idx)=",len(bad_feature_idx))
print(bad_feature_idx)
with open(bad_feat_storage_file,"w") as dest:
    dest.write(",".join([str(int(x)) for x in bad_feature_idx]))