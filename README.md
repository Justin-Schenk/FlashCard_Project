# Flashcard Web Application (CS 361 Microservices Project)

## Overview

This project is a microservices-based flashcard web application built for CS 361 over an 8-week period.  
The goal was to practice software engineering concepts (requirements, design, testing) and microservice architecture while building a usable study tool for language vocabulary and other subjects.

The app lets a user:

- Upload flashcards from a CSV file
- Create individual Q/A cards via a web form
- Review cards one at a time and track correctness
- Shuffle the deck for randomized practice
- Delete all stored flashcards when starting over

The project is a work in progress and intentionally written to be readable for other students.

---

## Tech Stack

- **Backend:** Python, Flask, Flask-CORS, pandas  
- **Frontend:** HTML, minimal inline JavaScript  
- **Storage:** CSV files (`flashcards.csv`, `shuffled_flashcards.csv`)  
- **Architecture:** Multiple Flask microservices + a simple UI service

---

## Architecture

The application is split into a UI app and four microservices:

- `main.py` – UI service  
  - Serves `index.html`, `create_flashcards.html`, `review_flashcards.html`, `settings.html`, `results.html` on `http://localhost:5000`

- `flashcard_creation_service.py` (port **5001**)  
  - Upload flashcards from CSV  
  - Create new Q/A pairs from a web form  
  - Persist data to `flashcards.csv`

- `flashcard_review_service.py` (port **5002**)  
  - Serve the “next” flashcard  
  - Track correct / incorrect / skipped answers  
  - Expose simple review statistics

- `flashcard_delete_service.py` (port **5003**)  
  - Delete all flashcards (reset `flashcards.csv` to just the header row)

- `flashcard_shuffle_service.py` (port **5004**)  
  - Shuffle the deck while keeping questions and answers paired  
  - Maintain a “shuffle session” that the UI can query

The HTML pages interact with these services using `fetch()` calls to the appropriate `localhost` ports.

---

## Getting Started

### Prerequisites

- Python 3.8+  
- `pip` (Python package manager)

### Installation

```bash
# Clone the repository
git clone https://github.com/Justin-Schenk/FlashCard_Project.git
cd FlashCard_Project

# Install dependencies
pip install flask flask-cors pandas
```
Running the Services

### Open five terminals in this directory and run:

# 1. UI service
python main.py

# 2. Creation service (port 5001)
python flashcard_creation_service.py

# 3. Review service (port 5002)
python flashcard_review_service.py

# 4. Delete service (port 5003)
python flashcard_delete_service.py

# 5. Shuffle service (port 5004)
python flashcard_shuffle_service.py


Then open a browser and visit:

http://localhost:5000


You should see the home page with navigation to create, review, and settings.
