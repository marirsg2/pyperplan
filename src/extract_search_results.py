"""
read fastdownward and pyperplan output and pull out
1) initial heuristic,
2) number of search nodes expanded
3) plan length
"""
"""
For fastdownward
1) the initial heuristic is from the first line that has  "new best heuristic value"
    eg:[t=0.00239439s, 9936 KB] New best heuristic value for lmcount(lm_factory = lm_rhw(reasonable_orders = true), transform = adapt_costs(one), pref = false): 14
    
    after seeing "Solution found!" we look for plan length and number of expanded nodes
    
2) "Plan length" eg: [t=0.00351264s, 9936 KB] Plan length: 18 step(s).
3) [t=0.00351264s, 9936 KB] Expanded 32 state(s).
"""
"""
For pyperplan
1) 2020-11-30 18:25:16,044 INFO     Initial h value: 19.000000
after "Goal reached"
2) 2020-11-30 18:25:59,441 INFO     Plan length: 21
3) 2020-11-30 18:25:59,441 INFO     47 Nodes expanded
"""

import os


FdSolutions = "../Data_storage/v1_GripperFDSolutionSet"
PyperPlanSolutions  = "../Data_storage/set1_v1_Gripper_GenFeat_solution_set"
# all_solution_folders = [PyperPlanSolutions]
all_solution_folders = [FdSolutions,PyperPlanSolutions]
idx_to_planner_name_dict = {0:"Fastdownward",1:"PyP_GenFeatures"}
problem_solution_dict = {} #will be a nested dictionary. the keys are 1) problem 2) planner 3) result metrics (initial heuristic, nodes expanded, plan length)
for solution_folder_idx in range(len(all_solution_folders)):
    solution_folder = all_solution_folders[solution_folder_idx]
    planner_name = idx_to_planner_name_dict[solution_folder_idx]
    for filename in os.listdir(solution_folder):
        if not "solution" in filename.lower():
            continue
        #---
        problem_name = "_".join([x for x in filename.split(".")[0].split("_") if len(x)<5])
        # if "n1_r3_o7_1" == problem_name:
        #     print("catch")
        if problem_name not in problem_solution_dict.keys():
            problem_solution_dict[problem_name] = {}
        if planner_name not in problem_solution_dict[problem_name].keys():
            problem_solution_dict[problem_name][planner_name] = {}
        solution_file_path = os.path.join(solution_folder, filename)
        found_solution = False
        found_heuristic = False
        initial_heuristic = 0
        plan_length = 0
        nodes_expanded = 0
        #make sure all strings are LOWER CASE
        with open(solution_file_path,"r") as src:
            all_lines = src.readlines()
            for single_line in all_lines:
                lowercase_line = single_line.lower().strip("\n")
                # if "heuristic" in lowercase_line:
                #     print(lowercase_line)
                if not found_heuristic:
                    if "initial h value" in lowercase_line or "new best heuristic" in lowercase_line:
                        found_heuristic = True
                        initial_heuristic = [int(float(x)) for x in
                                lowercase_line.strip("\n").split(" ") if
                                x.replace(".","").isnumeric()][-1]
                        continue # no more info on this line
                if "solution found" in lowercase_line or "goal reached" in lowercase_line:
                    found_solution = True
                    continue #other information will be in subsequent lines
                #end if
                if found_solution:
                    if "plan length" in lowercase_line:
                        parts = lowercase_line.split("plan length")[-1]
                        plan_length = [int(x) for x in parts.split(" ") if x.isnumeric()][-1]
                    if "expanded"  in lowercase_line:
                        nodes_expanded = [int(x) for x in lowercase_line.split(" ") if x.isnumeric()][-1]
        #---end with
        problem_solution_dict[problem_name][planner_name]["init_h"] = initial_heuristic
        problem_solution_dict[problem_name][planner_name]["expanded"] = nodes_expanded
        problem_solution_dict[problem_name][planner_name]["length"] = plan_length
    #-end for loop through solution files
#-end for loop through solution folders
# print(problem_solution_dict)
for problem in problem_solution_dict.keys():
    for planner_name in problem_solution_dict[problem].keys():
        print(problem, planner_name , problem_solution_dict[problem][planner_name])
    print("-------------")



