from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Path to the CSV file
FLASHCARDS_FILE = 'flashcards.csv'

# Load flashcards from CSV
def load_flashcards():
    if os.path.exists(FLASHCARDS_FILE):
        return pd.read_csv(FLASHCARDS_FILE)
    return pd.DataFrame(columns=['question', 'answer'])

# Save flashcards to CSV
def save_flashcards(flashcards):
    flashcards.to_csv(FLASHCARDS_FILE, index=False)

# Endpoint to delete a specific flashcard by question
@app.route('/delete_flashcard', methods=['DELETE'])
def delete_flashcard():
    try:
        # Get the question to delete from the request
        data = request.get_json()
        if 'question' not in data:
            return jsonify({"error": "Missing 'question' in request"}), 400
        question_to_delete = data['question']

        # Load existing flashcards
        flashcards = load_flashcards()

        # Check if the question exists
        if question_to_delete not in flashcards['question'].values:
            return jsonify({"error": "Flashcard not found"}), 404

        # Remove the flashcard
        flashcards = flashcards[flashcards['question'] != question_to_delete]

        # Save updated flashcards back to the file
        save_flashcards(flashcards)

        return jsonify({"message": "Flashcard deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to delete all flashcards except the header
@app.route('/delete_all_flashcards', methods=['DELETE'])
def delete_all_flashcards():
    try:
        # Keep only the header row
        flashcards = pd.DataFrame(columns=['question', 'answer'])
        save_flashcards(flashcards)

        return jsonify({"message": "All flashcards deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5003, debug=True)
