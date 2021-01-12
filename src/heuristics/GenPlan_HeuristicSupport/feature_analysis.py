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
import scipy.stats
from torch.utils.data import DataLoader
import warnings
warnings.simplefilter('error')



EPSILON = 1e-20 #zero is actually 1e-20. This was to avoid div by zero error.
train_data_file = "../GenPlan_data/JPMC_GenPlan_Blocksworld.p"
removable_feat_storage_file = "./blocksworld_no_change_feat_indexes.csv"
preprocessed_data_loc = train_data_file.replace(".p", "_preprocessed.p")

train_data_file = "../GenPlan_data/JPMC_GenPlan_gripper_singleSetting_varyRoomsBalls_40k.p"
removable_feat_storage_file = "./gripper_no_change_feat_indexes.csv"
preprocessed_data_loc = train_data_file.replace(".p", "_preprocessed2.p")

with open(preprocessed_data_loc,"rb") as src:
    torch_dataset = pickle.load(src)
    input_mean = pickle.load(src)
    input_std = pickle.load(src)
    output_mean = pickle.load(src)
    output_std = pickle.load(src)


train_loader = DataLoader(torch_dataset, batch_size=len(torch_dataset))
dataset = next(iter(train_loader))[0].numpy()
for i in range(1, 10):
    print(" ".join([str(x) for x in dataset[i]]))

input_std = input_std.detach().numpy()
bad_feature_idx = np.array(np.where(input_std == EPSILON)[0],dtype=int)

#compute the correlation between two features
correlated_features = []
for i in range(input_std.shape[0]):
    if i in correlated_features or i in bad_feature_idx:
        continue
    data_a = dataset[:,i]
    for j in range(i+1,input_std.shape[0]):
        if j in correlated_features or j in bad_feature_idx:
            continue
        data_b = dataset[:, j]
        pearsons_corr_data = scipy.stats.pearsonr(data_a,data_b)
        if pearsons_corr_data[0] > 0.99:
            correlated_features.append(j)
#end for loop

print("total num features = ", input_std.shape)
print("len(bad_feature_idx)=",len(bad_feature_idx))
print("len(correlated_features)=",len(correlated_features))

all_removable_features = list(bad_feature_idx)+list(correlated_features)
all_removable_features = sorted(all_removable_features)
print("len(all_removable_features)=",len(all_removable_features))
with open(removable_feat_storage_file, "w") as dest:
    dest.write(",".join([str(int(x)) for x in all_removable_features]))