Flashcard Web Application

Overview

This project was developed as part of the CS361 course over the span of approximately 8 weeks during an 11-week term. The goal was to apply concepts of microservices and software engineering to create a fully functional flashcard web application. It is truly a work in progress.

Technologies Used

Backend: Flask (Python)

Frontend: HTML, CSS, JavaScript

Data Storage: CSV files

Microservices

The application is structured into different microservices to handle various tasks efficiently:

Flashcard Creation Service: Handles creating and storing flashcards in the CSV file.

Flashcard Review Service: Manages the review process, including displaying flashcards, revealing answers, and marking responses as correct or incorrect.

Flashcard Shuffle Service: Handles shuffling flashcards for a session, ensuring questions and answers remain paired and providing a randomized review experience.

Flashcard Deletion Service: Allows users to delete all stored flashcards.

Application Structure

HTML Files: Provide the user interface for different parts of the application, such as creating flashcards, reviewing them, viewing results, and accessing settings.

JavaScript: Manages user interactions, such as fetching flashcards, revealing answers, shuffling, and submitting responses. All JavaScript is centralized in an external file for maintainability.

CSS: Improves the visual appeal of the application, giving it a modern and clean look. Flashcards are styled to look like real cards, with borders, rounded corners, and shadows.

Backend (Flask Services): Flask routes handle different operations, such as managing flashcards, shuffling sessions, and handling user input.

Installation

Prerequisites

Python 3.x

Flask

Pandas

Instructions

Clone the repository:

git clone <repository-url>
cd flashcard-web-app

Install the required Python packages:

pip install flask pandas

Run the Microservices:

Start each Flask service by navigating to the directory and running:

python flashcard_creation_service.py
python flashcard_review_service.py
python flashcard_shuffle_service.py
python flashcard_delete_service.py

Ensure each service runs on a different port as configured in the files.

Access the Application:
Open a web browser and navigate to http://localhost:5000 to start using the application.

Usage

Home Page: Provides navigation options to create new flashcards, review existing ones, shuffle the order, or view statistics.

Settings: Access options to delete all flashcards, reset statistics, or start/end a shuffle session.

Review Flashcards: This page shows each flashcard in a "box" styled to look like a card. Users can click "Reveal Answer" to view the answer, and mark their response accordingly.

Visual Design Enhancements

Flashcard Styling: Flashcards are displayed in a box with rounded corners, shadows, and padding to resemble physical cards. (work in progress currently)

Question and Answer: When revealing the answer, the question text is grayed out, and the answer is prominently displayed below to simulate a real flashcard experience.

Buttons and Navigation: The buttons are styled for consistency and ease of use, leveraging CSS or Bootstrap for enhanced visual appeal.

Future Improvements

User Authentication: Allow users to log in and save their progress across sessions.

Category-based Flashcards: Enable users to create flashcards grouped by categories or subjects. Multiple selectable flashcard files seperated by subject.

Export and Import: Add functionality to export flashcards to a file or import from an existing set. Creating more options for multiple subjects or flashcard files.

Progress Analytics: Provide detailed analytics for users to track their performance over time.

Contributing

If you want to contribute to this project, please fork the repository and submit a pull request. Contributions are welcome!

License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Contact

For any questions, suggestions, or issues, please open an issue on the repository or contact the project maintainer.


