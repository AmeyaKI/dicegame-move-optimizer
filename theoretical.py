from itertools import product
from game_rules import RuleEvaluator
import numpy as np
from functools import lru_cache
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import joblib, sys

# OVERVIEW: Running theoretical simulations (best move calculator - upload later)


sys.setrecursionlimit(50000) # increase recursive depth


RULES = RuleEvaluator()

ALL_DICE_COMBINATIONS = {i: [tuple(p) for p in product([1,2,3,4,5,6], repeat=i)] for i in range(7)}

###### MEMOIZATION AND EFFICIENCY FUNCTIONS######
def canonical(tup):
    return tuple(sorted(tup))

def merge_score_maps(base, child, offset):
    """
    base: dict(score -> count)
    child: dict(score -> count)
    offset: points to add to all child scores
    """
    for score, count in child.items():
        new_score = score + offset
        base[new_score] = base.get(new_score, 0) + count
    return base

@lru_cache(None)
def cached_check_roll(dice_tuple):
    return tuple(RULES.check_roll(np.array(dice_tuple)))


###### SIMULATION PROPER ######
@lru_cache(None)
def simulate(dice_tuple, reset_count=2):
    dice_tuple = canonical(dice_tuple)

    if len(dice_tuple) == 0:
        return {0: 1}  # Only 1 outcome: 0 points

    roll_results = cached_check_roll(dice_tuple)

    # CASE 1: No possible scores --> turn ends
    if len(roll_results) == 0:
        return {0: 1}


    # CASE 2: Scoring options exist --> tree recurse on each
    aggregate = {}

    for dice_value, num_dice, points in roll_results:
        remaining_dice = len(dice_tuple) - (num_dice if dice_value != 'all' else num_dice)

        # MAX 2 resets
        if remaining_dice == 0 and reset_count < 2: # MAXIMUM of 2 resets
            child_map = {}
            for new_roll in ALL_DICE_COMBINATIONS[6]:
                sub_map = simulate(new_roll, reset_max=reset_count + 1)
                merge_score_maps(aggregate, child_map, 0)
            merge_score_maps(aggregate, child_map, offset=points)
            
        elif remaining_dice == 0:
            child_map = {0: 1}
            merge_score_maps(aggregate, child_map, points)
            
        else:
            for new_roll in ALL_DICE_COMBINATIONS[remaining_dice]:
                child_map = simulate(new_roll)
                merge_score_maps(aggregate, child_map, offset=points)

    return aggregate

    
        
###### VISUALIZATION ######
def distribution_plotter(score_map, starting_roll):
    scores = np.array(list(score_map.keys()))
    counts = np.array(list(score_map.values()))
    
    # Calculate percentage for histogram
    total_paths = counts.sum()
    percentages = 100 * counts / total_paths
    
    # Find outliers (1.5IQR Rule)
    quartile_one = np.percentile(scores, 25)
    quartile_three = np.percentile(scores, 75)
    iqr = quartile_three - quartile_one
    upper_bound = quartile_three + 1.5 * iqr
    lower_bound = quartile_one - 1.5 * iqr
    
    outlier_mask = scores > upper_bound
    outlier_scores = scores[outlier_mask]
    outlier_percentages = percentages[outlier_mask]

    # Create bar chart for normal scores
    normal_mask = ~outlier_mask
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=scores[normal_mask],
        y=percentages[normal_mask],
        name="Scores",
        marker_color='skyblue',
        hovertemplate='%{y:.2f}% of paths<extra>Score: %{x}</extra>'
    ))

    # Overlay red points for outliers
    if len(outlier_scores) > 0:
        fig.add_trace(go.Scatter(
            x=outlier_scores,
            y=outlier_percentages,
            mode='markers',
            marker=dict(color='red', size=12),
            name='Outliers',
            hovertemplate='%{y:.5f}% of paths<extra>Outlier Score: %{x}</extra>'
        ))

    fig.update_layout(
        title=f"Distribution of Total Scores for {starting_roll}",
        xaxis_title="Total Score",
        yaxis_title="Percentage of Paths (%)",
        bargap=0,  # no gap between bars
        template="plotly_white"
    )

    fig.write_image(f"Distribution_{starting_roll}.png")
    fig.show()

def main():
    starting_roll = tuple()
    np.random.seed(42)

    initial_input = input("Enter 'Random' or 'Custom': ").strip().lower()
    
    if initial_input == 'random':
        starting_roll = tuple(np.random.randint(low=1, high=7, size=6).tolist())
    
    elif initial_input == 'custom':
        rolls = []
        for n in range(1, 7):
            user_input = input(f"Number {n}: ")
            rolls.append(int(user_input))
        
        starting_roll = tuple(rolls)
    
    else:
        raise ValueError("Incorrect Input. Terminating Program")
    
    print(f"Starting Roll: {starting_roll}")
    
    starting_roll_canonical = canonical(starting_roll)

    filename = f"theoretical_results_{starting_roll}.pkl"
    
    try: 
        result_map = joblib.load(filename)
        print("Loaded saved results.")
    except FileNotFoundError:
        print(f"Computing Result Map for {starting_roll}")
        result_map = simulate(starting_roll_canonical)
        joblib.dump(result_map, filename)
        print("Results saved.")
     
    
    print(f"Distinct scores: {len(result_map)}")
    print(f"All distinct scores: {sorted(int(k) for k in result_map.keys())}")
    print(f"Total paths counted: {sum(result_map.values())}")
    
    distribution_plotter(result_map, starting_roll)
    
    
if __name__ == '__main__':
    main()