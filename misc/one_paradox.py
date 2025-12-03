# fry dice game
import numpy as np 
import itertools as it



####### COMPLEX NOTES #######
# 6 dice: [1, 1, a, b, c, d]


# tree recursoin: 
    # either you keep two dice that r 1 --> 200 AND roll 4 
    # or you keep 1 dice that r 1 --> 100 AND roll 5 
    
    # need toget 350 --> else 0
    
# creat eclass
# total rules:
# 1 1 --> 100
# 3 1s --> 1000
# 3 of any other # --> 100 * #
# 1 5 --> 50
    
# create distribution of every permutation

distribution_1 = np.array([])
distribution_2 = np.array([])

one_dice_values = np.array([1, 2, 3, 4, 5, 6])


##########################################################################################

# single recursion
num_dice = 6

option_1 = np.array([1]) # keep 1 1 ---> 100 AND roll 5 dice
option_2 = np.array([1, 1]) # keep 2 1s ---> 200 AND roll 4 dice

real_perms_1, real_perms_2 = np.array([]), np.array([])
total_perms_1 = np.array(list(it.permutations(one_dice_values, num_dice - len(option_1))))

real_perms_1 = np.vstack(
    [np.concatenate((option_1, perm)) for perm in total_perms_1]
)

total_perms_2 = np.array(list(it.permutations(one_dice_values, num_dice - len(option_2))))

real_perms_2 = np.vstack(
    [np.concatenate((option_2, perm)) for perm in total_perms_2]
)
# EACH RECURISONN:
    # RETURN value + recurse
    
    # future RETURN: list of values + recurse (eliminate selected valuye)




