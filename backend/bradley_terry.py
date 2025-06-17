import numpy as np

def calculate_scores(objects, comparisons):
    """
    Calculates the Bradley-Terry scores for a set of objects and comparisons.

    Args:
        objects (list): A list of object names.
        comparisons (list): A list of dictionaries, where each dictionary
                            has a 'winner' and 'loser' key.

    Returns:
        dict: A dictionary mapping object names to their scores.
    """
    if not comparisons:
        return {obj: 1 for obj in objects}

    object_to_int = {obj: i for i, obj in enumerate(objects)}
    int_to_object = {i: obj for i, obj in enumerate(objects)}
    num_objects = len(objects)

    wins = np.zeros((num_objects, num_objects))
    for comp in comparisons:
        winner_idx = object_to_int[comp['winner']]
        loser_idx = object_to_int[comp['loser']]
        wins[winner_idx, loser_idx] += 1

    scores = np.ones(num_objects)
    for _ in range(100):  # 100 iterations should be enough for convergence
        total_wins = wins.sum(axis=1)
        
        denominator = np.zeros(num_objects)
        for i in range(num_objects):
            for j in range(num_objects):
                if i == j:
                    continue
                denominator[i] += (wins[i, j] + wins[j, i]) / (scores[i] + scores[j])

        # Add a small epsilon to avoid division by zero
        scores = total_wins / (denominator + 1e-9)

        # Normalize scores
        scores /= np.sum(scores)

    return {int_to_object[i]: score for i, score in enumerate(scores)} 