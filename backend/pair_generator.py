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
    Gets a new set of disjoint pairs for a user.
    Ensures no pair is shown to more than one user.
    """
    all_pairs = get_all_pairs(objects)
    used_pairs = get_used_pairs()

    available_pairs = [p for p in all_pairs if p not in used_pairs]
    random.shuffle(available_pairs)

    new_pairs_for_user = []
    used_objects_for_user = set()
    
    for pair in available_pairs:
        if pair[0] not in used_objects_for_user and pair[1] not in used_objects_for_user:
            new_pairs_for_user.append(pair)
            used_objects_for_user.add(pair[0])
            used_objects_for_user.add(pair[1])

    num_pairs_to_return = len(objects) // 2
    selected_pairs = new_pairs_for_user[:num_pairs_to_return]

    # Update the master list of used pairs
    for pair in selected_pairs:
        used_pairs.add(pair)
    save_used_pairs(used_pairs)

    return selected_pairs
