# Implementation Plan & Milestones

## 1. Project Setup & Refactoring
- [ ] Initialize Git repository and make initial commit. (DONE)
- [ ] Create `LLMmeta` directory and planning notes. (DONE)
- [ ] Create `data` directory for persistent storage. (DONE)
- [ ] Create `tests` directory and add `pytest` to `requirements.txt`.
- [ ] Create `backend/pair_generator.py`.
- [ ] Create `backend/compute_rankings.py`.
- [ ] Refactor `backend/app.py` to remove on-the-fly result calculation and results page.
- [ ] Add `uuid` to `requirements.txt`.

## 2. User Identity & Session Management
- [ ] Implement UUID generation for new users in `backend/app.py`.
- [ ] Use Flask sessions to store the `user_id`.

## 3. Data Persistence
- [ ] Modify `/api/compare` to write to `data/comparisons.csv`.
- [ ] Modify `/api/compare` to write to `data/comparisons.jsonl`.

## 4. Pair Sampling Logic
- [ ] Implement logic to track used pairs (e.g., in a `data/used_pairs.json` file).
- [ ] Implement the disjoint pair selection algorithm in `backend/pair_generator.py`.
- [ ] Integrate the new pair generator with the `/api/pairs` endpoint in `backend/app.py`.

## 5. Manual Ranking Script
- [ ] Implement `backend/compute_rankings.py` to read data and calculate scores.
- [ ] Add CLI arguments for input file paths.

## 6. Testing
- [ ] Write unit tests for `bradley_terry.py`.
- [ ] Write unit tests for `pair_generator.py`.
- [ ] Write integration tests for the Flask app workflow. 