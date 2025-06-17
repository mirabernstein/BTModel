import pytest
import json
import os
from backend.app import app as flask_app
from backend import app as app_module

# Test data
TEST_OBJECTS = ['test_obj1', 'test_obj2', 'test_obj3', 'test_obj4']

@pytest.fixture
def app():
    # Patch the app's objects for testing
    app_module.OBJECTS = TEST_OBJECTS

    flask_app.config.update({
        "TESTING": True,
    })

    # Clean up data files before each test
    if os.path.exists('data/comparisons.csv'):
        os.remove('data/comparisons.csv')
    if os.path.exists('data/comparisons.jsonl'):
        os.remove('data/comparisons.jsonl')

    yield flask_app

    # Clean up after each test
    if os.path.exists('data/comparisons.csv'):
        os.remove('data/comparisons.csv')
    if os.path.exists('data/comparisons.jsonl'):
        os.remove('data/comparisons.jsonl')


@pytest.fixture
def client(app):
    return app.test_client()

def test_full_user_flow(client):
    """
    Tests the full flow of a user getting pairs, making a choice,
    and having that choice be recorded.
    """
    # 1. User visits the root, gets a session cookie
    res = client.get('/')
    assert res.status_code == 200
    assert 'session' in res.headers['Set-Cookie']

    # 2. User fetches pairs
    res = client.get('/api/pairs')
    assert res.status_code == 200
    pairs = res.get_json()
    assert len(pairs) == len(TEST_OBJECTS) / 2
    
    # 3. User makes a comparison
    first_pair = pairs[0]
    winner, loser = first_pair[0], first_pair[1]
    res = client.post('/api/compare', 
                      data=json.dumps({'winner': winner, 'loser': loser, 'pair': tuple(sorted(first_pair))}),
                      content_type='application/json')
    assert res.status_code == 200
    assert res.get_json()['status'] == 'success'

    # 4. Verify data was written
    with open('data/comparisons.csv', 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 2 # Header + at least one data row
        last_line = lines[-1]
        assert winner in last_line
        assert loser in last_line

    # 5. User makes a second comparison
    second_pair = pairs[1]
    winner, loser = second_pair[0], second_pair[1]
    res = client.post('/api/compare', 
                      data=json.dumps({'winner': winner, 'loser': loser, 'pair': tuple(sorted(second_pair))}),
                      content_type='application/json')
    
    # 6. At this point, session['pairs'] is empty.
    # When user fetches pairs again, a new batch should be generated.
    res = client.get('/api/pairs')
    assert res.status_code == 200
    remaining_pairs = res.get_json()
    assert len(remaining_pairs) == len(TEST_OBJECTS) / 2

    # No need to clean up here, fixture does it 