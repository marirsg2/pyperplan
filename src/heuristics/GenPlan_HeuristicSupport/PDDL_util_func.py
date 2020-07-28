
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
        all_obj = []
        for proposition in state:
            all_obj += proposition.split("_")[1:]
        for obj in all_obj:
            dest.write(" "+obj)
        dest.write("\n)\n")
        #now we have written all objects
        dest.write("(:init\n")
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