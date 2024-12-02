import pandas as pd
import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable to hold shuffled flashcards during a session
shuffled_flashcards = []
session_active = False

FLASHCARDS_FILE = 'flashcards.csv'
SHUFFLED_FILE = 'shuffled_flashcards.csv'

@app.route('/shuffle_flashcards_session', methods=['POST'])
def shuffle_flashcards_session():
    global session_active
    try:
        # Load the flashcards from the CSV file
        if os.path.exists(FLASHCARDS_FILE):
            flashcards = pd.read_csv(FLASHCARDS_FILE, encoding='utf-8')
        else:
            return jsonify({"error": "No flashcards available to shuffle."}), 404

        # Check if there are enough flashcards to shuffle
        if len(flashcards) < 2:
            return jsonify({"error": "Not enough flashcards to shuffle."}), 400

        # Ensure the flashcards have the required columns ("question" and "answer")
        required_columns = {"question", "answer"}
        if not required_columns.issubset(flashcards.columns):
            return jsonify({"error": "Flashcards file is missing required columns."}), 500

        # Shuffle the flashcards (keeping question-answer pairs intact)
        shuffled_flashcards = flashcards.sample(frac=1, random_state=None)

        # Save shuffled flashcards to the shuffled file
        shuffled_flashcards.to_csv(SHUFFLED_FILE, index=False, encoding='utf-8')

        # Verify that the file has been written successfully and contains data
        if os.path.exists(SHUFFLED_FILE) and os.stat(SHUFFLED_FILE).st_size > 0:
            session_active = True
            return jsonify({"message": "Flashcards shuffled for the session."}), 200
        else:
            return jsonify({"error": "Failed to save shuffled flashcards."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/is_session_active', methods=['GET'])
def is_session_active():
    return jsonify({"session_active": session_active}), 200

@app.route('/get_shuffled_flashcards', methods=['GET'])
def get_shuffled_flashcards():
    if session_active:
        return jsonify(shuffled_flashcards), 200
    else:
        return jsonify({"error": "No active shuffle session."}), 404

@app.route('/end_shuffle_session', methods=['POST'])
def end_shuffle_session():
    global shuffled_flashcards, session_active
    try:
        shuffled_flashcards = []
        session_active = False
        return jsonify({"message": "Session shuffle ended. Back to original order."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5004, debug=True)
