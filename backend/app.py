from flask import Flask, render_template, jsonify, request, session
import os
import itertools
import uuid
import csv
from datetime import datetime, timezone
from .bradley_terry import calculate_scores
from . import pair_generator

app = Flask(__name__,
            template_folder=os.path.abspath('frontend/templates'),
            static_folder=os.path.abspath('frontend/static'))

# This should be a long, random string.
app.secret_key = 'dev' 

# In a real application, you would get this from a database or a configuration file.
OBJECTS = ['puppy1.jpg', 'puppy2.jpg', 'puppy3.jpg', 'puppy4.jpg']
comparisons = []

@app.route('/')
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/api/objects')
def get_objects():
    return jsonify(OBJECTS)

@app.route('/api/pairs')
def get_pairs():
    if 'user_id' not in session:
        return jsonify({"error": "user not initialized"}), 400

    if 'pairs' not in session or not session['pairs']:
        session['pairs'] = pair_generator.get_new_pairs_for_user(OBJECTS)
    
    return jsonify(session['pairs'])

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.json
    winner = data.get('winner')
    loser = data.get('loser')
    pair = tuple(sorted(data.get('pair', [])))
    user_id = session.get('user_id', 'unknown')
    timestamp = datetime.now(timezone.utc).isoformat()

    if winner and loser and pair:
        # Remove pair from session
        if 'pairs' in session:
            session['pairs'] = [p for p in session['pairs'] if tuple(sorted(p)) != pair]
            session.modified = True

        # Log to CSV
        csv_file = 'data/comparisons.csv'
        file_exists = os.path.isfile(csv_file)
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists or os.path.getsize(csv_file) == 0:
                writer.writerow(['user_id', 'timestamp', 'winner', 'loser'])
            writer.writerow([user_id, timestamp, winner, loser])

        # Log to JSONL
        with open('data/comparisons.jsonl', 'a') as f:
            f.write(f'{{"user_id": "{user_id}", "timestamp": "{timestamp}", "winner": "{winner}", "loser": "{loser}"}}\n')

        return jsonify({'status': 'success'})
        
    return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 