import pytest
from backend.bradley_terry import calculate_scores

def test_calculate_scores_no_comparisons():
    objects = ['a', 'b', 'c']
    comparisons = []
    scores = calculate_scores(objects, comparisons)
    assert scores['a'] == pytest.approx(1.0)
    assert scores['b'] == pytest.approx(1.0)
    assert scores['c'] == pytest.approx(1.0)

def test_calculate_scores_simple_ranking():
    objects = ['a', 'b']
    # 'a' beats 'b' once
    comparisons = [{'winner': 'a', 'loser': 'b'}]
    scores = calculate_scores(objects, comparisons)
    assert scores['a'] > scores['b']

def test_calculate_scores_transitive_ranking():
    objects = ['a', 'b', 'c']
    # a > b, b > c
    comparisons = [
        {'winner': 'a', 'loser': 'b'},
        {'winner': 'b', 'loser': 'c'}
    ]
    scores = calculate_scores(objects, comparisons)
    assert scores['a'] > scores['b'] > scores['c']

def test_calculate_scores_circular_ranking():
    objects = ['a', 'b', 'c']
    # a > b, b > c, c > a
    comparisons = [
        {'winner': 'a', 'loser': 'b'},
        {'winner': 'b', 'loser': 'c'},
        {'winner': 'c', 'loser': 'a'}
    ]
    scores = calculate_scores(objects, comparisons)
    # In a perfect circular dependency, scores should be equal
    assert scores['a'] == pytest.approx(scores['b'])
    assert scores['b'] == pytest.approx(scores['c']) 