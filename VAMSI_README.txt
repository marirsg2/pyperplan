1) The NN training is done in src/heuristics/GenPlan_HeuristicSupport/Gripper_GPfeatures_NN.py
    in the class GP_NN_heuristic_model_class(torch.nn.Module): you can add your changes


2) Run that file first to train the data,
    make sure the location to daniel's code is set correctly. this is the variable lisp_feature_gen_base_folder

3) Then run pyperplan.py.
     if it complains for any python lib dependencies, please install those