import requests
import pandas as pd
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import random

# Function to load flashcards from CSV
def load_flashcards(file_path):
    try:
        if os.path.exists(file_path):
            flashcards = pd.read_csv(file_path, encoding='utf-8').to_dict(orient='records')
            return flashcards
        else:
            return []
    except FileNotFoundError:
        return []

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

FLASHCARDS_FILE = 'flashcards.csv'
SHUFFLED_FILE = 'shuffled_flashcards.csv'  # Temporary shuffled file
current_index = 0
saved_index = 0  # Track the original index before shuffling
review_stats = {"correct": 0, "incorrect": 0, "skipped": 0, "total_attempts": 0}
question_revealed = False  # To control the sequence of reviewing
current_flashcard = None
shuffle_session_active = False

# Load the first flashcard on startup if available
flashcards = load_flashcards(FLASHCARDS_FILE)
if flashcards:
    current_flashcard = flashcards[0]

# Endpoint to get the next flashcard
@app.route('/review/next', methods=['GET'])
def next_flashcard():
    global current_index, question_revealed, current_flashcard

    # Determine whether the shuffle session is active
    try:
        response = requests.get('http://localhost:5004/is_session_active')
        response_data = response.json()
        if response_data.get("session_active"):
            file_to_load = SHUFFLED_FILE
        else:
            file_to_load = FLASHCARDS_FILE
    except Exception as e:
        return jsonify({"error": f"Error checking shuffle session status: {str(e)}"}), 500

    # Load flashcards based on the current session state
    flashcards = load_flashcards(file_to_load)

    # Ensure flashcards are available
    if not flashcards:
        return jsonify({"error": "No flashcards available."}), 404

    # Check if all questions have been reviewed
    if current_index >= len(flashcards):
        return jsonify({"error": "All questions have been reviewed"}), 200

    # Set the current flashcard
    current_flashcard = flashcards[current_index]

    # Ensure the current flashcard has the necessary keys
    if not current_flashcard or "question" not in current_flashcard or "answer" not in current_flashcard:
        return jsonify({"error": "Invalid flashcard format."}), 500

    question_revealed = False  # Reset the reveal flag for the new question
    return jsonify({"question": current_flashcard["question"], "index": current_index}), 200

# Endpoint to reveal the answer for the current flashcard
@app.route('/review/reveal', methods=['GET'])
def reveal_answer():
    global current_index, question_revealed, current_flashcard

    # Ensure current_flashcard is available
    if not current_flashcard:
        return jsonify({"error": "No flashcard selected. Use /review/next first."}), 400

    # Prevent revealing the answer multiple times
    if question_revealed:
        return jsonify({"error": "Answer already revealed. Please mark the answer as correct or incorrect."}), 400

    # Reveal the answer for the current flashcard
    question_revealed = True  # Set the reveal flag to prevent repeated reveals
    return jsonify({"question": current_flashcard["question"], "answer": current_flashcard["answer"]}), 200

# Endpoint to submit whether the answer was correct or incorrect
@app.route('/review/submit', methods=['POST'])
def submit_answer():
    global current_index, review_stats, question_revealed, current_flashcard
    data = request.get_json()

    if "correct" not in data:
        return jsonify({"error": "Missing 'correct' field in request"}), 400

    # Ensure that the answer was revealed before allowing submission
    if not question_revealed:
        return jsonify({"error": "Please reveal the answer before submitting."}), 400

    # Record the user's answer and update stats
    if data["correct"]:
        review_stats["correct"] += 1
    else:
        review_stats["incorrect"] += 1

    review_stats["total_attempts"] += 1

    # Move to the next flashcard
    current_index += 1
    current_flashcard = None
    question_revealed = False  # Reset the reveal flag for the next question

    return jsonify({"message": "Answer recorded successfully"}), 200

# Endpoint to skip the current flashcard
@app.route('/review/skip', methods=['POST'])
def skip_flashcard():
    global current_index, review_stats, question_revealed, current_flashcard

    # Load flashcards based on the current session state
    file_to_load = SHUFFLED_FILE if shuffle_session_active else FLASHCARDS_FILE
    flashcards = load_flashcards(file_to_load)

    # Ensure flashcards are available
    if not flashcards:
        return jsonify({"error": "No flashcards available."}), 404

    # Prevent skipping after the answer has been revealed
    if question_revealed:
        return jsonify({"error": "Cannot skip after revealing the answer. Please mark as correct or incorrect."}), 400

    # Record the skip and update stats
    review_stats["skipped"] += 1
    review_stats["total_attempts"] += 1

    # Move to the next flashcard
    current_index += 1

    # Ensure the current index is within bounds
    if current_index >= len(flashcards):
        return jsonify({"error": "All questions have been reviewed"}), 200

    # Set the current flashcard
    current_flashcard = flashcards[current_index]
    question_revealed = False  # Reset the reveal flag for the next question

    return jsonify({"message": "Question skipped successfully"}), 200

# Endpoint to end the review session and return the results
@app.route('/review/end', methods=['POST'])
def end_review_session():
    global review_stats, shuffle_session_active

    # End shuffle session if it was active
    if shuffle_session_active:
        shuffle_session_active = False
        if os.path.exists(SHUFFLED_FILE):
            os.remove(SHUFFLED_FILE)

    return jsonify({
        "message": "Review session ended.",
        "total_questions": review_stats["total_attempts"],
        "correct": review_stats["correct"],
        "incorrect": review_stats["incorrect"],
        "skipped": review_stats["skipped"]
    }), 200

# Endpoint to get review results for GET requests
@app.route('/review/results', methods=['GET'])
def get_review_results():
    global review_stats

    return jsonify({
        "total_questions": review_stats["total_attempts"],
        "correct": review_stats["correct"],
        "incorrect": review_stats["incorrect"],
        "skipped": review_stats["skipped"]
    }), 200

@app.route('/review/reset', methods=['POST'])
def reset_review_session():
    global current_index, review_stats, question_revealed

    # Reset session variables
    current_index = 0
    review_stats = {"correct": 0, "incorrect": 0, "skipped": 0, "total_attempts": 0}
    question_revealed = False

    return jsonify({"message": "Review session has been reset."}), 200

if __name__ == '__main__':
    app.run(port=5002, debug=True)

