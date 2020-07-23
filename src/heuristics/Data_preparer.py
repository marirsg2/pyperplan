
#----------NO DO THIS IN THE TRACE GENERATION CODE
# import pickle
#
#
# data_source = "JPMC_GenPlan_100c2_s4_p1_a1_logistics_dataset.p"
# unprocessed_data = None
# with open(data_source, "rb") as src:
#     unprocessed_data = pickle.load(src)
#
# converted_data = []
# #now convert each data point in a larger set of points
# for single_seq,goal in unprocessed_data:
#     for seq_idx in range(len(single_seq)):
#         converted_data.append((single_seq[seq_idx],goal,len(single_seq)-seq_idx+1))
# #end for loop
#
#
#
