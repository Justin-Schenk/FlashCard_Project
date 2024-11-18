from flask import Flask, request, jsonify
from flask_cors import CORS
import csv

app = Flask(__name__)
CORS(app)

# In-memory storage and tracking
flashcards = []  # Stores all flashcards as {question, answer}
current_index = 0  # Tracks the current flashcard index
review_stats = {"correct": 0, "incorrect": 0}  # Tracks review progress

# Function to load flashcards from CSV
def load_flashcards():
    global flashcards, current_index, review_stats
    try:
        with open('flashcards.csv', 'r') as file:
            reader = csv.DictReader(file)
            flashcards = [{"question": row["question"], "answer": row["answer"]} for row in reader]
        current_index = 0  # Reset to the first flashcard
        review_stats = {"correct": 0, "incorrect": 0}  # Reset stats
    except FileNotFoundError:
        flashcards = []
    except Exception as e:
        print(f"Error loading flashcards: {e}")

# Endpoint to get the next flashcard
@app.route('/review/next', methods=['GET'])
def next_flashcard():
    global current_index

    # Reload flashcards if not already loaded
    if not flashcards:
        load_flashcards()

    # Check if all questions have been answered
    if current_index >= len(flashcards):
        return jsonify({"error": "All questions have been reviewed"}), 200

    # Return the current flashcard question without modifying the index
    flashcard = flashcards[current_index]
    return jsonify({"question": flashcard["question"]}), 200

# Endpoint to reveal the answer for the current flashcard
@app.route('/review/reveal', methods=['GET'])
def reveal_answer():
    global current_index

    if not flashcards:
        return jsonify({"error": "No flashcards available."}), 404

    # Ensure current_index is valid
    if current_index < len(flashcards):
        return jsonify({"answer": flashcards[current_index]["answer"]}), 200
    else:
        return jsonify({"error": "No flashcard selected. Use /review/next first."}), 400

# Endpoint to submit whether the answer was correct or incorrect
@app.route('/review/submit', methods=['POST'])
def submit_answer():
    global current_index, review_stats
    data = request.get_json()
    if "correct" not in data:
        return jsonify({"error": "Missing 'correct' field in request"}), 400

    if data["correct"]:
        review_stats["correct"] += 1
    else:
        review_stats["incorrect"] += 1

    # Increment current_index to point to the next flashcard
    current_index += 1

    # Check if all questions have been reviewed
    if current_index >= len(flashcards):
        return jsonify({"message": "All questions reviewed"}), 200

    return jsonify({"message": "Answer recorded successfully"}), 200

# Endpoint to end the review session and return results
@app.route('/end_review', methods=['GET'])
def end_review():
    global current_index, review_stats
    total = len(flashcards)
    correct = review_stats["correct"]
    incorrect = review_stats["incorrect"]

    # Reset the session
    current_index = 0
    review_stats = {"correct": 0, "incorrect": 0}

    return jsonify({
        "total": total,
        "correct": correct,
        "incorrect": incorrect
    }), 200

# Load flashcards at startup
load_flashcards()

if __name__ == '__main__':
    app.run(port=5002, debug=True)
