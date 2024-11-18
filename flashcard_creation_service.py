from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Path to the CSV file used for persistent storage
FLASHCARDS_FILE = 'flashcards.csv'

# In-memory storage for flashcards
flashcards = pd.DataFrame(columns=['question', 'answer'])

# Load flashcards from the CSV file at startup
def load_flashcards():
    global flashcards
    if os.path.exists(FLASHCARDS_FILE):
        flashcards = pd.read_csv(FLASHCARDS_FILE)
    else:
        flashcards = pd.DataFrame(columns=['question', 'answer'])

# Save flashcards to the CSV file
def save_flashcards():
    global flashcards
    flashcards.to_csv(FLASHCARDS_FILE, index=False)

# Endpoint to manually add a single flashcard
@app.route('/add_flashcard', methods=['POST'])
def add_flashcard():
    try:
        question = request.form.get('question')
        answer = request.form.get('answer')

        if not question or not answer:
            return jsonify({"error": "Both 'question' and 'answer' are required"}), 400

        # Add the new flashcard to the in-memory storage
        global flashcards
        new_flashcard = pd.DataFrame([{'question': question, 'answer': answer}])
        flashcards = pd.concat([flashcards, new_flashcard], ignore_index=True)

        # Save the updated flashcards to the CSV file
        save_flashcards()

        return jsonify({"message": "Flashcard added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint to view all flashcards (for debugging purposes)
@app.route('/flashcards', methods=['GET'])
def get_flashcards():
    try:
        return jsonify(flashcards.to_dict(orient='records')), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Load flashcards at startup
load_flashcards()

if __name__ == '__main__':
    app.run(port=5001, debug=True)
