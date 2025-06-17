import csv
import bradley_terry
import argparse

def main():
    parser = argparse.ArgumentParser(description="Compute Bradley-Terry scores from comparison data.")
    parser.add_argument('data_file', nargs='?', default='data/comparisons.csv',
                        help='Path to the comparison data file (CSV).')
    args = parser.parse_args()

    try:
        with open(args.data_file, 'r') as f:
            reader = csv.reader(f)
            header = next(reader) # Skip header
            comparisons = [{'winner': row[2], 'loser': row[3]} for row in reader]
    except FileNotFoundError:
        print(f"Error: Data file not found at {args.data_file}")
        return
    except Exception as e:
        print(f"Error reading data file: {e}")
        return

    if not comparisons:
        print("No comparison data found.")
        return

    objects = set()
    for comp in comparisons:
        objects.add(comp['winner'])
        objects.add(comp['loser'])
    
    scores = bradley_terry.calculate_scores(list(objects), comparisons)
    sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)

    print("Bradley-Terry Rankings:")
    for obj, score in sorted_scores:
        print(f"{obj}: {score:.4f}")

if __name__ == '__main__':
    main()
