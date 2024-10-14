===============================
Learning Progress Tracker Project
===============================

This project is a Python-based application designed to manage students and track their progress across multiple courses. It provides functionalities to add students, validate their credentials, track course progress, notify students upon course completion, and display statistics about course popularity, student activity, and difficulty.

Project Features
----------------

The Learning Progress Tracker has the following core features:

1. **Student Management:**

   - Add new students by providing first name, last name, and email.
   - Validate input to ensure all names and email addresses follow the proper format.
   - Ensure each email is unique among students.

2. **Course Progress Tracking:**

   - Track students' progress across four courses: `Python`, `DSA` (Data Structures & Algorithms), `Databases`, and `Flask`.
   - Record the number of submissions and update progress points for each student.
   - Determine if a student has enrolled in a course based on their submission history.

3. **Notifications:**

   - Notify students once they have completed a course.
   - Keep track of which students have been notified to avoid redundant messages.

4. **Statistics and Course Analysis:**

   - Display statistics such as the most and least popular courses.
   - Analyze the highest and lowest student activity in each course.
   - Identify the easiest and hardest courses based on the average scores from submissions.

5. **Completion Tracking:**

   - Determine when students have completed a course based on their progress points.
   - Notify students automatically upon course completion.

Installation Guide
------------------

**Prerequisites**

To run the Learning Progress Tracker, you need the following installed:

- **Python 3.1+**
- **Conda** (optional, for creating an isolated environment)
- **unittest** (Python's built-in testing module)

**Setup Steps**

1. **Cloning the Repository:**

   Clone the project repository using the following command:

   .. code-block:: bash

      git clone <repository-url>

2. **Creating a New Conda Environment** (optional):

   To create a new isolated environment for this project:

   .. code-block:: bash

      conda create --name progress_tracker python=3.12

   This will create an environment named ``progress_tracker`` with Python 3.12 installed.

3. **Activating the Environment:**

   Activate the created environment using the following command:

   .. code-block:: bash

      conda activate progress_tracker

4. **Installing Additional Packages:**

   If you decide to use additional packages, install them via `pip`:

   .. code-block:: bash

      pip install <package-name>

5. **Running the Application:**

   You can run the main program using the following command:

   .. code-block:: bash

      python learning_progress_tracker.py

   This will launch the tracker and prompt for input commands to manage students and track their course progress.

User Commands
-------------

After starting the program, the following commands are available:

- **add students**: Add multiple students by inputting their first name, last name, and email.
- **list**: List all students by their unique IDs.
- **add points**: Assign points to a student for their submissions in the four courses.
- **find**: Search for a student by their ID to view their course progress.
- **statistics**: View statistics about the courses, such as the most popular or least popular courses, highest and lowest activity, and course difficulty.
- **notify**: Notify students who have completed any of the four courses.

Example Usage
-------------

Here is an example session demonstrating how to use the tracker:

.. code-block:: text

   Learning Progress Tracker
   Enter command: add students
   Enter student credentials or 'back' to return:
   John Doe john.doe@example.com
   The student has been added.
   Enter student credentials or 'back' to return:
   Jane Smith jane.smith@example.com
   The student has been added.
   Enter student credentials or 'back' to return:
   back
   Total 2 students were added

   Enter command: list
   Students:
   123456789
   987654321

   Enter command: add points
   Enter an id and points or 'back' to return:
   123456789 600 200 50 0
   Points updated.

   Enter command: back

   Enter command: statistics
   Most popular: Python, DSA
   Least popular: Flask
   Highest activity: Python
   Lowest activity: Flask
   Easiest course: Python
   Hardest course: DSA

   Enter command: back

   Enter command: notify
   To: john.doe@example.com
   Re: Your Learning Progress
   Hello, John Doe! You have accomplished our Python course!

Running Unit Tests
------------------

This project includes a set of unit tests for validating the functionality of the classes and methods. To run the tests, navigate to the project directory and use the following command:

.. code-block:: bash

   python -m unittest test_learning_progress_tracker.py

The tests will validate student management, course progress, and notifications.

Directory Structure
-------------------

The project directory contains the following files:

.. code-block:: text

   ├── learning_progress_tracker.py      # Main application file
   ├── test_learning_progress_tracker.py # Unit tests for the application
   ├── README.rst                        # Project documentation
   ├── .gitignore                        # Git ignore rules
   └── LICENSE                           # Project license

Contributing
------------

Contributions to this project are welcome. If you find a bug or have a feature request, please submit an issue on the project repository.

License
-------

This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_ file for details.
