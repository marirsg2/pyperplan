
"""
Logistics preamble example
(define (problem logistics-c4-s3-p2-a1)
(:domain logistics-strips)
(:objects a0
          c0 c1 c2 c3
          t0 t1 t2 t3
          l00 l01 l02 l10 l11 l12 l20 l21 l22 l30 l31 l32
          p0 p1
)
"""



#================================================================================================
def convert_to_gripper_problem_file(state,goal,dest_problem_file):
    """
    state and goal are described by a set of tuples. Each tuple contains a predicate which is true in the current state or goal def
    """
    with open(dest_problem_file, "w") as dest:

        #first write the preamble
        dest.write("(define (problem gripper)\n")
        dest.write("(:domain gripper-strips)\n")
        dest.write("(:objects\n")

        #collect all objects in the state

        temp_obj_dict = {"robot":set(),"gripper":set(),"room":set(),"ball":set()}
        for proposition in state:
            temp_objs = proposition.split("_")[1:]
            for single_obj in temp_objs:
                for single_key in temp_obj_dict.keys():
                    if single_key in single_obj:
                        temp_obj_dict[single_key].add(single_obj) #first letter is the key
        #end loop through propositions

        for obj_type in temp_obj_dict.keys():
            curr_line = "  "
            for single_obj in temp_obj_dict[obj_type]:
                curr_line += single_obj + " "
            curr_line += "  - " + obj_type + "\n"
            dest.write(curr_line)
        #end for loop through obj types
        dest.write(")\n")
        #now we have written all objects
        dest.write("(:init\n")
        state = sorted(state)
        for proposition in state:
            dest.write("(" + proposition.replace("_", " ") + ")\n")
        dest.write(")\n")
        # dest.write("(:goal\n(and\n")
        dest.write("(:goal\n")  # there is no need for "and" in this application
        for proposition in goal:
            dest.write("(" + proposition.replace("_", " ") + ")\n")
        dest.write(")\n")  # close goal
        dest.write(")")  # close problem file
#=============================
#================================================================================================
def convert_to_logistics_problem_file(state,goal,dest_problem_file):
    """
    state and goal are described by a set of tuples. Each tuple contains a predicate which is true in the current state or goal def
    """
    with open(dest_problem_file, "w") as dest:

        #first write the preamble
        dest.write("(define (problem logistics)\n")
        dest.write("(:domain logistics-strips)\n")
        dest.write("(:objects\n")

        #collect all objects in the state

        temp_obj_dict = {"c":set(),"l":set(),"t":set(),"a":set(),"p":set()}
        type_decoder_dict = {"c":"city","l":"location","t":"truck","a":"airplane","p":"package"}
        for proposition in state:
            temp_objs = proposition.split("_")[1:]
            for single_obj in temp_objs:
                temp_obj_dict[single_obj[0]].add(single_obj) #first letter is the key
        #end loop through propositions

        for obj_type_letter in temp_obj_dict.keys():
            curr_line = "  "
            for single_obj in temp_obj_dict[obj_type_letter]:
                curr_line += single_obj + " "
            curr_line += "  - TYP" + type_decoder_dict[obj_type_letter] + "\n"
            dest.write(curr_line)
        #end for loop through obj types
        dest.write(")\n")
        #now we have written all objects
        dest.write("(:init\n")
        state = sorted(state)
        for proposition in state:
            dest.write("(" + proposition.replace("_", " ") + ")\n")
        dest.write(")\n")
        # dest.write("(:goal\n(and\n")
        dest.write("(:goal\n")  # there is no need for "and" in this application
        for proposition in goal:
            dest.write("(" + proposition.replace("_", " ") + ")\n")
        dest.write(")\n")  # close goal
        dest.write(")")  # close problem file
#=============================