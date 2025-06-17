from flask import Flask, render_template, jsonify, request
import os
import itertools
from .bradley_terry import calculate_scores

app = Flask(__name__,
            template_folder=os.path.abspath('frontend/templates'),
            static_folder=os.path.abspath('frontend/static'))

# In a real application, you would get this from a database or a configuration file.
OBJECTS = ['puppy1.jpg', 'puppy2.jpg', 'puppy3.jpg', 'puppy4.jpg']
comparisons = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/objects')
def get_objects():
    return jsonify(OBJECTS)

@app.route('/api/pairs')
def get_pairs():
    pairs = list(itertools.combinations(OBJECTS, 2))
    return jsonify(pairs)

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.json
    winner = data.get('winner')
    loser = data.get('loser')
    if winner and loser:
        comparisons.append({'winner': winner, 'loser': loser})
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Invalid data'}), 400

@app.route('/results')
def results():
    return render_template('results.html')

@app.route('/api/results')
def api_results():
    scores = calculate_scores(OBJECTS, comparisons)
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return jsonify(sorted_scores)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 