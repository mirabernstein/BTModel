import itertools
import json
import os
import random

USED_PAIRS_FILE = 'data/used_pairs.json'

def get_all_pairs(objects):
    """Generates all possible pairs of objects, sorted."""
    return [tuple(sorted(p)) for p in itertools.combinations(objects, 2)]

def get_used_pairs():
    """Loads the set of used pairs from the file."""
    if not os.path.exists(USED_PAIRS_FILE) or os.path.getsize(USED_PAIRS_FILE) == 0:
        return set()
    with open(USED_PAIRS_FILE, 'r') as f:
        try:
            used_pairs_list = json.load(f)
            return {tuple(p) for p in used_pairs_list}
        except json.JSONDecodeError:
            return set()

def save_used_pairs(pairs):
    """Saves the set of used pairs to the file."""
    with open(USED_PAIRS_FILE, 'w') as f:
        json.dump(list(pairs), f)

def get_new_pairs_for_user(objects):
    """
    Gets a new set of disjoint pairs for a user by shuffling the object list.
    This is fast and scalable.
    """
    if len(objects) < 2:
        return []

    # Create a mutable copy and shuffle it
    shuffled_objects = list(objects)
    random.shuffle(shuffled_objects)

    # Create disjoint pairs from the shuffled list
    new_pairs = []
    for i in range(0, len(shuffled_objects) - 1, 2):
        new_pairs.append(tuple(sorted((shuffled_objects[i], shuffled_objects[i+1]))))

    return new_pairs
