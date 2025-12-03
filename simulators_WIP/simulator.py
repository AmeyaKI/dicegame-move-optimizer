# fry dice game
import numpy as np 
import itertools as it
from game_rules import RuleEvaluator
import matplotlib.pyplot as plt

RULES = RuleEvaluator()

# save: array of rolls, total points 

roll_1 = np.array([1, 1, 5, 6, 3, 4]) # keep the 1 --> recurse the rest s
roll_2 = np.array([1, 1, 5, 6, 3, 4]) # keep the 2 -> recurse ther rest


# IMP NOTE: Each time roll recurses --> have to calculate permutations all over again

 
# EXPERIMENTAL VERSION
def simulate_game(dice_rolls, depth=0):
    indent = "  " * depth
    print(f"{indent}Dice: {dice_rolls}")
    
    if len(dice_rolls) == 0:
        print(f"{indent}→ No dice left. Return [0]")
        return [0]
    
    roll_results = RULES.check_roll(dice_rolls)
    print(f"{indent}Scoring options: {roll_results}")

    
    if len(roll_results) == 0:
        new_dice_rolls = np.random.randint(1, 7, size = len(dice_rolls) -1)
        print(f"{indent}No scoring options → Reroll with {new_dice_rolls}")

        return simulate_game(new_dice_rolls)
    
    all_scores = []
    
    for [dice_value, num_dice, points] in roll_results:
        print(f"{indent}→ Use {num_dice} dice of value {dice_value}, worth {points} points")

        new_roll_len = len(dice_rolls) - num_dice
        
        new_dice_rolls = np.random.randint(1, 7, size = len(dice_rolls) - new_roll_len)
        print(f"{indent}  Remaining dice count: {new_roll_len}, new roll: {new_dice_rolls}")

        sub_scores = simulate_game(new_dice_rolls)
        
        for s in sub_scores:
            branch_score = points + s
            print(f"{indent}  Branch score: {points} + {s} = {branch_score}")

            all_scores.append(branch_score)
            
            
    print(f"{indent}Return scores: {all_scores}")
    return all_scores
 
# def distribution_plotter(all_scores):
#     plt.figure(figsize=(10, 6))
#     plt.bar(scores, counts)
#     plt.xlabel("Total Score")
#     plt.ylabel("Number of Paths")
#     plt.title("Distribution of Total Score Across All Dice Combinations")
#     plt.grid(axis='y')
#     plt.tight_layout()
#     plt.show()


 
 
 
 
 
 
 
 
 
 
# FUTURE:
    # if 3 > num_dice > 1 --> iterate thru  num_dice twice   
     
    # can choose number of dice to remove 
    # ie. if you have 2 5s --> choose between removing 1 5 or both 5s
        # INCORPROATE LATER

 
    # rules.check()
    
    # tree recursion:
        # keep one: 100 (from 1) + [everything but 1 1]
        # keep both ones: 200 (from 2 1s) + [everything but 2 1s]
    # ASSUME: When you don't get 2 1s, YOU CHOOSE




