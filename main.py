import CAfuncs as cpl
import random
from formattedrules import *

all_CA = []

for i in range(2):
    temp = []
    get_boring = False
    if i == 0: # Interesting
        get_boring = False # True
    else:
        get_boring = True
    all_survive, all_born, all_states = [],[],[]

    if get_boring:
        all_survive = survive_boor
        all_born = born_boor
        all_states = state_boor
    else:
        all_survive = survive_int
        all_born = born_int
        all_states = state_int
    for i in range(len(all_survive)):
        survive_arr = all_survive[i]
        born_arr = all_born[i]
        num_states = all_states[i]
        rerun = 0
        if get_boring:
            rerun = 10
        else:
            rerun = 30
        for num_iter in range(rerun):
            print("done initializing", flush=True)
            #num_states = random.randrange(9) + 2# 2,3,...,10
            #num_states = ... set it manually if desired

            print("num_states: " + str(num_states), flush=True)
            cellular_automaton = cpl.init_random2d_anyK(100, 100, num_states) # Returns a randomly initialized matrix with values consisting of numbers in {0,...,k - 1}. k = 2 by default (live and dead).

            # Populate survive and born arrays
            #survive_arr = [2, 3] # Conway's GOL : [2, 3]
            #born_arr = [3] # Conway's GOL : [3]

            # def fifty_fifty():
            #     "Return 0 or 1 with 50% chance for each"
            #     return random.randrange(2)

            #survive_arr = []
            #born_arr = []
            # for i in range(0, 8+1): # should start at 0. can be born with 0
            #     add_rule_bool = fifty_fifty()
            #     if add_rule_bool == 1:
            #         survive_arr.append(i)
            #
            # for i in range(0,8+1): # should start at 0
            #     add_rule_bool = fifty_fifty()
            #     if add_rule_bool == 1:
            #         born_arr.append(i)

            # MANUAL RULES HERE
            #survive_arr = [2, 3] # Conway's GOL : [2, 3]     #survive_arr =  [0, 2, 3,5,6,7,8]#[2,3,4,6,7,8]
                 #born_arr = [3,4,6,8]#[1,2,3,4,6,7,8]
            #born_arr = [3] # Conway's GOL : [3]


            print("Survive rules: " +str(survive_arr), flush=True)
            print("Born rules: " + str(born_arr), flush=True)

            # Create file name
            S_str = "S"
            for ele in survive_arr:
                S_str += str(ele)
            B_str = "B"
            for ele in born_arr:
                B_str += str(ele)
            States_str = "States" + str(num_states)
            Label_str = ""
            if get_boring:
                Label_str = "Boring"
            else:
                Label_str = "Interesting"
            sample_num = "Sample" + str(num_iter)  # number of times rerun. 10 times for boring. 30 times for interesting.


            image_name = Label_str + "/" +  S_str + "_" + B_str + "_" + States_str + "_" + Label_str + "_" + sample_num + "_"


            cellular_automaton = cpl.evolve2dMoore(cellular_automaton,  survive_arr, born_arr, num_states, timesteps=125,
                                          apply_rule = cpl.random_2d_rule, r = 1 , neighbourhood='Moore')
            print("done evolving", flush=True)
            cpl.plot2d_animate(cellular_automaton, image_name = image_name, begin_save = 80, end_save = 120)
