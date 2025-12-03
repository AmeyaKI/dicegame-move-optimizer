from functools import lru_cache
import numpy as np
from itertools import combinations_with_replacement
from game_rules import RuleEvaluator
import matplotlib.pyplot as plt

RULES = RuleEvaluator()
DICE_TOTAL = 6

def all_histograms(n):
    """Return all count histograms of n dice."""
    result = []
    for combo in combinations_with_replacement([1,2,3,4,5,6], n):
        counts = [0] * 6
        for v in combo:
            counts[v - 1] += 1
        result.append(tuple(counts))
    return result

ALL_HISTS = {i: all_histograms(i) for i in range(7)}

@lru_cache(maxsize=None)
def helper(remaining_dice: int, total_points: int) -> tuple[int]:
    if remaining_dice == 0:
        return (int(total_points),)
    
    totals = []
    
    for counts in ALL_HISTS[remaining_dice]:
        roll_results = RULES.check_roll_from_counts(list(counts))
        
        if len(roll_results) == 0:  # Bust
            totals.append(0)
            continue
        
        for dice_value, num_used, pts in roll_results:
            next_remaining = remaining_dice - num_used
            next_total = total_points + pts
            branch = helper(next_remaining, next_total)
            totals.extend([int(x) for x in branch])
    
    return tuple(totals)

def simulator(dice_rolls: np.ndarray) -> dict | int:
    initial_rolls = RULES.check_roll(dice_rolls)
    
    if len(initial_rolls) == 0:
        return 0
    
    scores_dict = {}
    
    for dice_value, num_dice, points in initial_rolls:
        remaining = DICE_TOTAL - num_dice
        outcomes = helper(remaining, points)
        scores_dict[(dice_value, num_dice, points)] = list(outcomes)
    
    return scores_dict

def create_distribution(scores: dict) -> None:
    
    first_key = next(iter(scores))
    
    plt.hist(scores[first_key])
    plt.title(f"Dice Roll: {first_key}")
    plt.xlabel("Point Distribution")
    plt.ylabel("Frequency")
    plt.savefig(f"Sim: {first_key}.png")
    plt.show()
    
    

def main():
    np.random.seed(42)
    dice_rolls = np.random.randint(1,7,6)
    
    print(f"Dice rolled: {dice_rolls}")
    
    scores_dict = simulator(dice_rolls)
    
    print("Possible move distributions:")
    for k,v in scores_dict.items(): # type: ignore
        print(f"{k} --> {v[:10]}...")
    
    create_distribution(scores_dict) # type: ignore

if __name__=="__main__":
    main()