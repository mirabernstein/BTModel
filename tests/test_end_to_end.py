import pytest
import random
import re
from backend.bradley_terry import calculate_scores
from backend.pair_generator import get_new_pairs_for_user

def parse_puppy_number(puppy_str):
    """Extracts the number from a puppy string like 'puppy1.jpg'."""
    return int(re.search(r'\d+', puppy_str).group())

def test_end_to_end_simulation():
    """
    Simulates a full experiment with a known probabilistic outcome
    and verifies the Bradley-Terry model's output.
    """
    objects = ['puppy1.jpg', 'puppy2.jpg', 'puppy3.jpg', 'puppy4.jpg']
    num_users = 20
    all_comparisons = []

    print("\n--- Starting End-to-End Simulation ---")
    print(f"Simulating {num_users} users comparing 4 objects.")

    for _ in range(num_users):
        # Each user gets N/2 disjoint pairs, just like in the real app
        user_pairs = get_new_pairs_for_user(objects)

        for pair in user_pairs:
            obj1_str, obj2_str = pair
            obj1_val = parse_puppy_number(obj1_str)
            obj2_val = parse_puppy_number(obj2_str)

            # Determine winner based on the probabilistic model p = i / (i + j)
            prob_obj1_wins = obj1_val / (obj1_val + obj2_val)
            
            if random.random() < prob_obj1_wins:
                winner, loser = obj1_str, obj2_str
            else:
                winner, loser = obj2_str, obj1_str
            
            all_comparisons.append({'winner': winner, 'loser': loser})
    
    print(f"Generated {len(all_comparisons)} total comparisons.")

    # Run the Bradley-Terry model on the simulated data
    scores = calculate_scores(objects, all_comparisons)
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    print("\n--- Bradley-Terry Model Results ---")
    for obj, score in sorted_scores:
        print(f"{obj}: {score:.4f}")

    # Verify that the ranking matches the known probabilistic model.
    # Note: Due to the stochastic nature of the simulation, this could
    # theoretically fail, but it's very unlikely with this many comparisons.
    result_order = [item[0] for item in sorted_scores]
    expected_order = ['puppy4.jpg', 'puppy3.jpg', 'puppy2.jpg', 'puppy1.jpg']
    
    assert result_order == expected_order
    print("\nAssertion successful: Final ranking matches expected order.")
    print("--- Simulation Complete ---\n") 