"""
pull all data from the target folder's subfolders and store as csv file
"""
import numpy
import os

main_source_folder = "../Data_storage/Gripper_results"
heuristic_set = set()
problem_solution_dict = {}

for heuristic_folder_name in [x[0] for x in os.walk(main_source_folder)][1:]:
    planner_name = heuristic_folder_name.split("_")[-1]
    heuristic_set.add(planner_name)
    for filename in os.listdir(heuristic_folder_name):
        problem_name = "_".join([x for x in filename.split(".")[0].split("_") if len(x) < 5])
        # if "n1_r3_o7_1" == problem_name:
        #     print("catch")
        if problem_name not in problem_solution_dict.keys():
            problem_solution_dict[problem_name] = {}
        if planner_name not in problem_solution_dict[problem_name].keys():
            problem_solution_dict[problem_name][planner_name] = {}
        found_solution = False
        found_heuristic = False
        initial_heuristic = 0
        plan_length = 0
        nodes_expanded = 0
        # make sure all strings are LOWER CASE
        with open(heuristic_folder_name + "/"+filename, "r") as src:
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
                                             x.replace(".", "").isnumeric()][-1]
                        continue  # no more info on this line
                if "solution found" in lowercase_line or "goal reached" in lowercase_line:
                    found_solution = True
                    continue  # other information will be in subsequent lines
                # end if
                if found_solution:
                    if "plan length" in lowercase_line:
                        parts = lowercase_line.split("plan length")[-1]
                        plan_length = [int(x) for x in parts.split(" ") if x.isnumeric()][-1]
                    if "expanded" in lowercase_line:
                        nodes_expanded = [int(x) for x in lowercase_line.split(" ") if x.isnumeric()][-1]
        # ---end with
        problem_solution_dict[problem_name][planner_name]["init_h"] = initial_heuristic
        problem_solution_dict[problem_name][planner_name]["expanded"] = nodes_expanded
        problem_solution_dict[problem_name][planner_name]["length"] = plan_length
    # -end for loop through solution files
# -end for loop through heuristic folders
#display results
for problem in problem_solution_dict.keys():
    for planner_name in problem_solution_dict[problem].keys():
        print(problem, planner_name , problem_solution_dict[problem][planner_name])
    print("-------------")