import unittest
import builtins
from typing import Optional, Tuple
from learning_progress_tracker import Student, StudentManager, CourseManager

class TestStudent(unittest.TestCase):
    """Tests for the Student class."""

    def test_valid_first_name(self):
        """Test that valid first names are recognized as valid."""
        self.assertTrue(Student.is_first_name_valid('John'))
        self.assertTrue(Student.is_first_name_valid('Anne-Marie'))
        self.assertTrue(Student.is_first_name_valid("O'Neill"))
        self.assertFalse(Student.is_first_name_valid('J'))
        self.assertFalse(Student.is_first_name_valid('John123'))
        self.assertFalse(Student.is_first_name_valid(''))

    def test_valid_last_name(self):
        """Test that valid last names are recognized as valid."""
        self.assertTrue(Student.is_last_name_valid('Doe'))
        self.assertTrue(Student.is_last_name_valid("O'Connor"))
        self.assertTrue(Student.is_last_name_valid('Smith-Jones'))
        self.assertFalse(Student.is_last_name_valid('D'))
        self.assertFalse(Student.is_last_name_valid('Doe1'))
        self.assertFalse(Student.is_last_name_valid(''))

    def test_valid_email(self):
        """Test that valid emails are recognized as valid."""
        self.assertTrue(Student.is_email_valid('john.doe@example.com'))
        self.assertTrue(Student.is_email_valid('alice@example.co.uk'))
        self.assertTrue(Student.is_email_valid('user+name@example.com'))
        self.assertFalse(Student.is_email_valid('john.doe'))
        self.assertFalse(Student.is_email_valid('john.doe@com'))
        self.assertFalse(Student.is_email_valid('john.doe@.com'))

    def test_update_points_and_submissions(self):
        """Test updating points and submissions for a student."""
        student = Student('John', 'Doe', 'john.doe@example.com')
        student.update_points((5, 10, 15, 20))
        self.assertEqual(student.progress, {'Python': 5, 'DSA': 10, 'Databases': 15, 'Flask': 20})
        self.assertEqual(student.submissions, {'Python': 1, 'DSA': 1, 'Databases': 1, 'Flask': 1})
        self.assertEqual(student.completed_courses, {'Python': False, 'DSA': False, 'Databases': False, 'Flask': False})
        self.assertEqual(student.notifications_sent, {'Python': False, 'DSA': False, 'Databases': False, 'Flask': False})

    def test_is_enrolled_in_course(self):
        """Test if the student is enrolled in a course."""
        student = Student('John', 'Doe', 'john.doe@example.com')
        # Initially, the student is not enrolled in any course (progress is 0)
        self.assertFalse(student.is_enrolled_in_course('Python'))
        self.assertFalse(student.is_enrolled_in_course('DSA'))

        # After updating points, the student should be enrolled in Python and Databases
        student.update_points((5, 0, 10, 0))
        self.assertTrue(student.is_enrolled_in_course('Python'))
        self.assertTrue(student.is_enrolled_in_course('Databases'))
        self.assertFalse(student.is_enrolled_in_course('DSA'))

class TestStudentManager(unittest.TestCase):
    """Tests for the StudentManager class."""

    def setUp(self):
        """Set up a StudentManager instance for testing."""
        self.manager = StudentManager()

    def test_add_student(self):
        """Test adding a valid and invalid student."""
        # Adding valid student
        result = self.manager.add_student('John', 'Doe', 'john.doe@example.com')
        self.assertEqual(result, 'Success')
        self.assertEqual(len(self.manager.students), 1)

        # Adding invalid student with invalid last name
        result = self.manager.add_student('John', 'D', 'john.doe2@example.com')
        self.assertEqual(result, 'Incorrect last name.')
        self.assertEqual(len(self.manager.students), 1)  # No additional student added

        # Adding invalid student with invalid email
        result = self.manager.add_student('Jane', 'Smith', 'jane.smith')
        self.assertEqual(result, 'Incorrect email.')
        self.assertEqual(len(self.manager.students), 1)  # No additional student added

        # Adding duplicate email
        result = self.manager.add_student('Jane', 'Doe', 'john.doe@example.com')
        self.assertEqual(result, 'This email is already taken.')
        self.assertEqual(len(self.manager.students), 1)  # No additional student added

    def test_list_students(self):
        """Test listing students."""
        self.manager.add_student('John', 'Doe', 'john.doe@example.com')
        self.manager.add_student('Alice', 'Smith', 'alice.smith@example.com')
        self.assertEqual(len(self.manager.students), 2)
        # Capture the output of list_student_ids
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output
        self.manager.list_student_ids()
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()
        # Check that the output contains the student IDs
        self.assertIn(str(self.manager.students[0].student_id), output)
        self.assertIn(str(self.manager.students[1].student_id), output)

    def test_user_input_splitter(self):
        """Test the user input splitter function."""
        self.assertEqual(self.manager.user_input_splitter('John Doe john@example.com'),
                         ('John', 'Doe', 'john@example.com'))
        self.assertEqual(self.manager.user_input_splitter('John Smith Jr. john.smith@example.com'),
                         ('John', 'Smith Jr.', 'john.smith@example.com'))
        self.assertIsNone(self.manager.user_input_splitter('JohnDoejohn@example.com'))
        self.assertIsNone(self.manager.user_input_splitter('John Doe'))

    def test_point_input_splitter(self):
        """Test the point input splitter function."""
        student_id = '12345'
        self.assertEqual(self.manager.point_input_splitter(f'{student_id} 10 20 30 40'),
                         (student_id, 10, 20, 30, 40))
        self.assertIsNone(self.manager.point_input_splitter(f'{student_id} 10 20 30'))
        self.assertIsNone(self.manager.point_input_splitter(f'{student_id} -10 20 30 40'))
        self.assertIsNone(self.manager.point_input_splitter(f'invalid_id 10 20 30 40'))
        self.assertIsNone(self.manager.point_input_splitter(f'{student_id} 10 20 30 40 50'))

    def test_find_student_by_id(self):
        """Test finding a student by ID."""
        self.manager.add_student('John', 'Doe', 'john.doe@example.com')
        student_id = self.manager.students[0].student_id
        student = self.manager.find_student_by_id(student_id)
        self.assertIsNotNone(student)
        self.assertEqual(student.email, 'john.doe@example.com')
        # Test with invalid ID
        student = self.manager.find_student_by_id(99999)
        self.assertIsNone(student)

    def test_add_points(self):
        """Test adding points to a student."""
        self.manager.add_student('John', 'Doe', 'john.doe@example.com')
        student_id = self.manager.students[0].student_id

        # Simulate input for add_points
        inputs = [
            f'{student_id} 10 20 30 40',
            'back'
        ]

        # Capture the output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        def mock_input(prompt=''):
            return inputs.pop(0)

        original_input = builtins.input  # Use builtins.input
        builtins.input = mock_input

        try:
            self.manager.add_points()
        finally:
            builtins.input = original_input  # Restore builtins.input
            sys.stdout = sys.__stdout__

        # Check that the student's progress and submissions are updated
        student = self.manager.find_student_by_id(student_id)
        self.assertEqual(student.progress, {'Python': 10, 'DSA': 20, 'Databases': 30, 'Flask': 40})
        self.assertEqual(student.submissions, {'Python': 1, 'DSA': 1, 'Databases': 1, 'Flask': 1})

    def test_find_student(self):
        """Test finding and displaying student information."""
        self.manager.add_student('John', 'Doe', 'john.doe@example.com')
        student = self.manager.students[0]
        student.update_points((10, 20, 30, 40))
        student_id = student.student_id

        # Simulate input for find_student
        inputs = [
            str(student_id),
            'back'
        ]

        # Capture the output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        def mock_input(prompt=''):
            return inputs.pop(0)

        original_input = builtins.input  # Use builtins.input
        builtins.input = mock_input

        try:
            self.manager.find_student()
        finally:
            builtins.input = original_input  # Restore builtins.input
            sys.stdout = sys.__stdout__

        output = captured_output.getvalue()
        # Check that the output contains the correct student information
        expected_output = f"{student_id} points: Python={student.progress['Python']}; DSA={student.progress['DSA']}; Databases={student.progress['Databases']}; Flask={student.progress['Flask']}"
        self.assertIn(expected_output, output)

class TestCourseManager(unittest.TestCase):
    """Tests for the CourseManager class."""

    def setUp(self):
        """Set up a CourseManager instance for testing."""
        self.student_manager = StudentManager()
        self.course_manager = CourseManager(self.student_manager)

        # Adding students
        self.student_manager.add_student('John', 'Doe', 'john.doe@example.com')
        self.student_manager.add_student('Jane', 'Smith', 'jane.smith@example.com')
        self.john = self.student_manager.students[0]
        self.jane = self.student_manager.students[1]

    def test_determine_course_completion(self):
        """Test that course completion is determined correctly."""
        # Update points to complete Python course for John
        self.john.update_points((600, 0, 0, 0))  # 100% completion in Python
        # Update points for Jane
        self.jane.update_points((0, 400, 0, 0))  # 100% completion in DSA

        # Determine course completion
        self.course_manager.determine_course_completion('Python')
        self.course_manager.determine_course_completion('DSA')

        self.assertTrue(self.john.completed_courses['Python'])
        self.assertFalse(self.john.completed_courses['DSA'])
        self.assertFalse(self.jane.completed_courses['Python'])
        self.assertTrue(self.jane.completed_courses['DSA'])

    def test_notify_students(self):
        """Test that notifications are sent correctly."""
        # Update points to complete courses
        self.john.update_points((600, 0, 0, 0))  # John completes Python
        self.jane.update_points((0, 400, 0, 0))  # Jane completes DSA

        # Capture the output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        # Call notify_students
        self.course_manager.notify_students()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Check that notifications were sent correctly
        expected_john_notification = f"To: {self.john.email}\nRe: Your Learning Progress\nHello, {self.john.first_name} {self.john.last_name}! You have accomplished our Python course!"
        expected_jane_notification = f"To: {self.jane.email}\nRe: Your Learning Progress\nHello, {self.jane.first_name} {self.jane.last_name}! You have accomplished our DSA course!"

        self.assertIn(expected_john_notification, output)
        self.assertIn(expected_jane_notification, output)
        self.assertIn("Total 2 students have been notified.", output)

        # Notifications should be marked as sent
        self.assertTrue(self.john.notifications_sent['Python'])
        self.assertTrue(self.jane.notifications_sent['DSA'])

        # Run notify_students again, should not send notifications
        captured_output = StringIO()
        sys.stdout = captured_output

        self.course_manager.notify_students()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Should indicate that 0 students have been notified
        self.assertIn("Total 0 students have been notified.", output)

    def test_notify_students_multiple_courses(self):
        """Test notifications when a student completes multiple courses."""
        # John completes Python and DSA
        self.john.update_points((600, 400, 0, 0))

        # Capture the output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        self.course_manager.notify_students()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Check that two notifications are sent to John
        expected_python_notification = f"To: {self.john.email}\nRe: Your Learning Progress\nHello, {self.john.first_name} {self.john.last_name}! You have accomplished our Python course!"
        expected_dsa_notification = f"To: {self.john.email}\nRe: Your Learning Progress\nHello, {self.john.first_name} {self.john.last_name}! You have accomplished our DSA course!"

        self.assertIn(expected_python_notification, output)
        self.assertIn(expected_dsa_notification, output)
        self.assertIn("Total 1 student have been notified.", output)  # Singular 'student' since only John is notified

    def test_get_completion_percentage(self):
        """Test calculation of completion percentage."""
        percentage_python = self.course_manager.get_completion_percentage('Python', 300)
        self.assertEqual(percentage_python, 50.0)

        percentage_dsa = self.course_manager.get_completion_percentage('DSA', 200)
        self.assertEqual(percentage_dsa, 50.0)

        percentage_databases = self.course_manager.get_completion_percentage('Databases', 480)
        self.assertEqual(percentage_databases, 100.0)

        percentage_flask = self.course_manager.get_completion_percentage('Flask', 275)
        self.assertEqual(percentage_flask, 50.0)

    def test_determine_enrolled_students(self):
        """Test determining enrolled students per course."""
        # Update points
        self.john.update_points((10, 20, 0, 40))  # John enrolled in Python, DSA, Flask
        self.jane.update_points((20, 0, 40, 30))  # Jane enrolled in Python, Databases, Flask

        python_students = self.course_manager.determine_enrolled_students('Python')
        self.assertIn(self.john, python_students)
        self.assertIn(self.jane, python_students)

        dsa_students = self.course_manager.determine_enrolled_students('DSA')
        self.assertIn(self.john, dsa_students)
        self.assertNotIn(self.jane, dsa_students)

        databases_students = self.course_manager.determine_enrolled_students('Databases')
        self.assertNotIn(self.john, databases_students)
        self.assertIn(self.jane, databases_students)

        flask_students = self.course_manager.determine_enrolled_students('Flask')
        self.assertIn(self.john, flask_students)
        self.assertIn(self.jane, flask_students)

    def test_display_course_details(self):
        """Test display_course_details method."""
        # Update points
        self.john.update_points((600, 0, 0, 0))  # John completes Python
        self.jane.update_points((300, 0, 0, 0))  # Jane partial completion in Python

        # Capture the output
        from io import StringIO
        import sys
        captured_output = StringIO()
        sys.stdout = captured_output

        self.course_manager.display_course_details('Python')

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Expected output contains header and student info
        self.assertIn('Python', output)
        self.assertIn('id', output)
        self.assertIn('points', output)
        self.assertIn('completed', output)
        self.assertIn(str(self.john.student_id), output)
        self.assertIn(str(self.jane.student_id), output)
        self.assertIn('100.0%', output)  # John's completion percentage
        self.assertIn('50.0%', output)   # Jane's completion percentage

    # Add other existing tests from previous code as needed

if __name__ == '__main__':
    unittest.main()