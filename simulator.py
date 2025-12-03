import numpy as np
import itertools as it
from game_rules import RuleEvaluator
from numpy import typing as npt

"""
ULTIMATE GOAL: tell user the best move
    ie. if you roll [1, 5, 6, 2, 3, 3]
        Whether to 
          keep the 1, roll the rest OR 
          keep the 5, roll the rest, OR 
          keep 1 and 5, roll rerst
    
    Create point distribution for each move
         {roll_result: [distribution of points]}
            Only preserve first roll_result in dictioanry, everything else keeps iterating till final # of pts reached
           
"""


roll = np.random.randint(1, 7, 6) # NOTE: replace this with the inference result of the model
begin = True

rules = RuleEvaluator()

def simulator(dice_rolls: npt.NDArray, starter=True):
    """_summary_
    Args:
        dice_rolls (npt.NDArray): numpy array of dice rolls
        starter (bool, optional): Whether the call to simulator() is the first or not 
        the first. 
            if it's the first, each roll_result in roll_results will be a key in return dict
            else simulator() will keep iterating and return point values
        Defaults to True.

    Returns:
        Dict: {roll_result: [point distribution]}
    """

    if len(dice_rolls) == 0:
        return 0
    
    roll_results = rules.check_roll(dice_rolls)
    if len(roll_results) == 0:
        return 0 # has to override previous rolls
    
    
    for dice_value, num_dice, points in roll_results:
        ...

    
def minimum_scores_evaluator(scores: dict, begin: bool = True):
    """Implements 350 and 1000 rule:
        if simulated_value: 0 points (begin=True) --> need to reach 1000 else 0 pts
        elif simulated_value: >1000 points (begin=False) -->  need to reach 350 pts else 0 pts
    """
    minimum = 1000 if begin else 350
    
    for key, value_list in scores.items():
        for i in range(len(value_list)): # iterate through list
            if value_list[i] < minimum:  
                value_list[i] = 0
        
  
def best_move(scores: dict):
    """Determine which move is the best by calculating statistics (tbd) from 
    each key's distribution in scores

    Args:
        scores (dict): _description_
    """
    ... 
    


