from flask import Flask, jsonify
import csv
import random

app = Flask(__name__)

# Shuffle/Randomize Flashcards Service
@app.route('/shuffle_flashcards', methods=['POST'])
def shuffle_flashcards():
    flashcards = []
    header = None  # Variable to store the header row

    try:
        # Read the flashcards from the CSV
        with open('flashcards.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # Read the header row
            for row in reader:
                flashcards.append(row)

        # Shuffle the flashcards (but leave the header intact)
        random.shuffle(flashcards)

        # Write the shuffled flashcards back to the CSV
        with open('flashcards.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)  # Write the header row first
            writer.writerows(flashcards)

        return jsonify({'message': "Flashcards shuffled successfully."}), 200

    except FileNotFoundError:
        return jsonify({'error': 'Flashcards file not found.'}), 404
    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {e}'}), 500

# Example usage
if __name__ == '__main__':
    app.run(port=5004, debug=True)
