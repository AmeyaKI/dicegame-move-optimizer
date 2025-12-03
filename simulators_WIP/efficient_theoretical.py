from itertools import product
import numpy as np
from functools import lru_cache
import matplotlib.pyplot as plt
import joblib, sys
from game_rules import RuleEvaluator

sys.setrecursionlimit(50000)  # deep recursion

RULES = RuleEvaluator()


###### HELPER FUNCTIONS ######
def dice_to_counts(dice_tuple):
    """Convert a dice tuple to canonical counts of faces 1-6."""
    counts = [0] * 6
    for d in dice_tuple:
        counts[d - 1] += 1
    return tuple(counts)


def counts_to_dice(counts):
    """Reconstruct a dice tuple from counts for iteration."""
    dice = []
    for i, c in enumerate(counts):
        dice.extend([i + 1] * c)
    return tuple(dice)


def merge_score_maps(base, child, offset):
    """Merge score dictionaries adding offset points."""
    for score, count in child.items():
        base[score + offset] = base.get(score + offset, 0) + count
    return base


def generate_counts_combinations(n):
    """Generate all unique dice count tuples for n dice."""
    counts_set = set()
    for roll in product(range(1, 7), repeat=n):
        counts_set.add(dice_to_counts(roll))
    return tuple(sorted(counts_set))


# Precompute unique dice counts for each dice number 0-6
ALL_DICE_COUNTS = {i: generate_counts_combinations(i) for i in range(7)}


###### SIMULATION FUNCTION ######
@lru_cache(None)
def simulate_counts(counts, enable_reset=True):
    total_dice = sum(counts)
    if total_dice == 0:
        return {0: 1}

    dice_tuple = counts_to_dice(counts)
    roll_results = RULES.check_roll(np.array(dice_tuple))

    if not roll_results:
        return {0: 1}  # turn ends if no scoring dice

    aggregate = {}

    for dice_value, num_dice, points in roll_results:
        new_counts = list(counts)
        if dice_value != 'all':
            new_counts[dice_value - 1] -= num_dice
            remaining_dice = sum(new_counts)
        else:
            # combined branch: remove all scoring dice
            for val, count, _ in roll_results:
                if val != 'all':
                    new_counts[val - 1] -= count
            remaining_dice = sum(new_counts)

        if remaining_dice == 0 and enable_reset:
            # 6-dice reset branch
            for new_roll_counts in ALL_DICE_COUNTS[6]:
                child_map = simulate_counts(new_roll_counts, enable_reset=True)
                merge_score_maps(aggregate, child_map, points)
        else:
            # normal recursion
            if remaining_dice > 0:
                child_map = simulate_counts(tuple(new_counts), enable_reset=enable_reset)
                merge_score_maps(aggregate, child_map, points)
            else:
                # If remaining_dice == 0 but reset disabled
                merge_score_maps(aggregate, {0: 1}, points)

    return aggregate


###### VISUALIZATION ######
def distribution_plotter(score_map, starting_roll):
    scores = list(score_map.keys())
    counts = list(score_map.values())
    total_paths = sum(counts)
    percentages = [100 * c / total_paths for c in counts]

    plt.figure(figsize=(10, 6))
    plt.bar(scores, percentages, width=50, color='skyblue', edgecolor='black', linewidth=0.5)
    plt.xlabel("Total Score")
    plt.ylabel("Percentage of Paths (%)")
    plt.title("Distribution of Total Scores")
    plt.xticks(range(min(scores), max(scores) + 1, 100))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f"Distribution_{starting_roll}.png")
    plt.show()


###### MAIN FUNCTION ######
def main():
    np.random.seed(42)
    initial_input = input("Enter 'Random' or 'Custom': ").strip().lower()

    if initial_input == 'random':
        starting_roll = tuple(np.random.randint(1, 7, size=6).tolist())
    elif initial_input == 'custom':
        rolls = [int(input(f"Number {n}: ")) for n in range(1, 7)]
        starting_roll = tuple(rolls)
    else:
        raise ValueError("Incorrect input")

    print(f"Starting Roll: {starting_roll}")
    counts_key = dice_to_counts(starting_roll)
    filename = f"theoretical_results_{starting_roll}.pkl"

    try:
        result_map = joblib.load(filename)
        print("Loaded saved results.")
    except FileNotFoundError:
        print(f"Computing Result Map for {starting_roll}...")
        result_map = simulate_counts(counts_key)
        joblib.dump(result_map, filename)
        print("Results saved.")

    # print(f"Distinct scores: {len(result_map)}")
    
    print("All distinct scores:")
    
    for score in sorted(result_map.keys()):
        print(score, end=", ")
    print()
    
    # print(f"Total paths counted: {sum(result_map.values())}")
    # distribution_plotter(result_map, starting_roll)


if __name__ == '__main__':
    main()