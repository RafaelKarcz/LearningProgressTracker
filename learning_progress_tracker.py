import re
from typing import List, Tuple, Optional

class Student:
    def __init__(self, first_name: str, last_name: str, email: str) -> None:
        """Initialize the student with first name, last name, and email."""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.student_id = abs(hash(email))
        self.progress = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
        self.submissions = {'Python': 0, 'DSA': 0, 'Databases': 0, 'Flask': 0}
        self.completed_courses = {'Python': False, 'DSA': False, 'Databases': False, 'Flask': False}
        self.notifications_sent = {'Python': False, 'DSA': False, 'Databases': False, 'Flask': False}

    @staticmethod
    def is_first_name_valid(first_name: str) -> bool:
        """Validate the student's first name using a regex pattern."""
        if re.fullmatch(r"[A-Za-z]+(['-][A-Za-z]+)*", first_name) and len(first_name) > 1:
            return all(len(part) > 1 for part in first_name.split(" "))
        return False

    @staticmethod
    def is_last_name_valid(last_name: str) -> bool:
        """Validate the student's last name using a regex pattern."""
        if re.fullmatch(r"[A-Za-z]+([' -][A-Za-z]+)*", last_name) and len(last_name) > 1:
            return all(len(part) > 1 for part in last_name.split(" "))
        return False

    @staticmethod
    def is_email_valid(email: str) -> bool:
        """Validate the student's email using a regex pattern."""
        return re.fullmatch(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z0-9]{1,}", email) is not None

    def update_points(self, points: Tuple[int, int, int, int]) -> None:
        """Update the learning progress for the student"""
        courses = ['Python', 'DSA', 'Databases', 'Flask']
        for i, course in enumerate(courses):
            if points[i] > 0:
                self.progress[course] += points[i]
                self.submissions[course] += 1
        
    def is_enrolled_in_course(self, course: str) -> bool:
        """Check if the student is enrolled in a given course."""
        return self.progress[course] > 0 


class StudentManager:
    def __init__(self) -> None:
        """Initialize the student manager with an empty list of students and a set of emails."""
        self.students: List[Student] = []
        self.emails: set = set()
        self.student_ids: dict = {}

    @staticmethod
    def user_input_splitter(user_input: str) -> Optional[Tuple[str, str, str]]:
        """Split the user input into first name, last name, and email."""
        try:
            first_name, last_name_and_email = user_input.split(' ', 1)
            last_name, email = last_name_and_email.rsplit(' ', 1)
            return first_name, last_name, email
        except ValueError:
            return None

    def add_student(self, first_name: str, last_name: str, email: str) -> str:
        """Add a single student if the credentials are valid and return specific error messages."""
        student = Student(first_name, last_name, email)
        # Check if the first name is valid
        if not Student.is_first_name_valid(first_name):
            return 'Incorrect first name.'
        # Check if the last name is valid
        if not Student.is_last_name_valid(last_name):
            return 'Incorrect last name.'
        # Check if the email is valid
        if not Student.is_email_valid(email):
            return 'Incorrect email.'
        # Check if the email is already in use
        if email in self.emails:
            return 'This email is already taken.'
        # Add the student if all credentials are valid
        self.students.append(student)
        self.emails.add(email)
        self.student_ids[email] = student.student_id
        return 'Success'

    def add_students(self) -> None:
        """Add students based on user input."""
        print("Enter student credentials or 'back' to return:")
        student_count = 0
        while True:
            user_input = input().strip()
            if user_input.lower() == 'back':
                break
            if not user_input or len(user_input.split(' ')) < 3:
                print('Incorrect credentials.')
                continue
            split_data = self.user_input_splitter(user_input)
            if not split_data:
                print('Incorrect credentials.')
                continue
            first_name, last_name, email = split_data
            result_message = self.add_student(first_name, last_name, email)
            if result_message == 'Success':
                student_count += 1
                print('The student has been added.')
            else:
                print(result_message)
        print(f'Total {student_count} students were added')

    def list_student_ids(self) -> None:
        """List all student ids."""
        if not self.students:
            print('No students found.')
        else:
            print('Students:')
            for student in self.students:
                print(student.student_id)

    def point_input_splitter(self, user_input: str) -> Optional[Tuple[str, int, int, int, int]]:
        """Split the user input into student_id and course points, but return student_id as string."""
        try:
            parts = user_input.split()
            if len(parts) != 5 or not parts[0].isdigit():
                return None
            student_id = parts[0]
            points = tuple(map(int, parts[1:]))
            if all(point >= 0 for point in points):
                return (student_id, *points)
            else:
                return None
        except (ValueError, TypeError):
            return None

    def find_student_by_id(self, student_id: int) -> Optional[Student]:
        """Find a student by their unique ID"""
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def add_points(self) -> None:
        """Add points to a specific student id"""
        print("Enter an id and points or 'back' to return")
        while True:
            user_command = input().strip()
            if user_command.lower() == 'back':
                break
            user_input = user_command.split()
            if len(user_input) < 5:
                print('Incorrect points format')
                continue
            student_id = user_input[0]
            try:
                student_id_int = int(student_id)
                student = self.find_student_by_id(student_id_int)
            except ValueError:
                student = None
            if student is None:
                print(f'No student is found for id={student_id}.')
                continue
            try:
                points = tuple(map(int, user_input[1:]))
                if len(points) != 4 or any(point < 0 for point in points):
                    print('Incorrect points format')
                    continue
            except ValueError:
                print('Incorrect points format')
                continue
            student.update_points(points)
            print('Points updated.')

    def find_student(self) -> None:
        """Output student information to the console based on the student id"""
        print("Enter an id or 'back' to return")
        while True:
            user_command = input().strip()
            if user_command.lower() == 'back':
                break
            original_id = user_command
            try:
                student_id = int(user_command)
            except ValueError:
                student_id = None
            student = self.find_student_by_id(student_id) if isinstance(student_id, int) else None
            if student is None:
                print(f'No student is found for id={original_id}.')
            else:
                course_points = student.progress
                print(f"{student_id} points: Python={course_points['Python']}; DSA={course_points['DSA']}; "
                      f"Databases={course_points['Databases']}; Flask={course_points['Flask']}")
    

class CourseManager:
    def __init__(self, student_manager: StudentManager) -> None:
        """Initialize the student manager with a set of the available courses and 
        empty dictionaries for popularity, student_activity, and difficulty"""
        self.courses: set = {'Flask', 'Databases', 'Python', 'DSA'}
        self.popularity: dict = {}
        self.student_activity: dict = {}
        self.difficulty: dict = {}
        self.student_manager = student_manager
    
    def determine_enrolled_students(self, course) -> list:
        """Determine the enrolled students for a specific course"""
        return list(filter(lambda s: s.is_enrolled_in_course(course), self.student_manager.students))
    
    def determine_course_popularity(self) -> None:
        """Determine the popularity of each course and update the self.popularity dictionary"""
        total_enrollments = 0
        for course in self.courses:
            enrolled_students = self.determine_enrolled_students(course)
            if enrolled_students:
                self.popularity[course] = len(enrolled_students)
                total_enrollments += len(enrolled_students)
            else:
                self.popularity[course] = 'n/a'
        if total_enrollments == 0:
            for course in self.courses:
                self.popularity[course] = 'n/a'
                
    def determine_valid_popularity(self) -> dict:
        """Return a dictionary of courses with valid popularity values"""
        return {course: value for course, value in self.popularity.items() if value != 'n/a'}

    def most_popular_course(self) -> list:
        """Find the courses with the highest amount of enrolled students"""
        self.determine_course_popularity()  # Ensure popularity data is up-to-date
        valid_popularity = self.determine_valid_popularity()
        if not valid_popularity:
            return ['n/a']
        max_value = max(valid_popularity.values())
        most_popular_courses = [course for course, value in self.popularity.items() if value == max_value]
        return most_popular_courses

    def least_popular_course(self) -> list:
        """Find the course with the least amount of enrolled students"""
        self.determine_course_popularity() # Ensure popularity data is up-to-date
        valid_popularity = self.determine_valid_popularity()
        if not valid_popularity:
            return ['n/a']
        min_value = min(valid_popularity.values())
        least_popular_courses = [course for course, val in valid_popularity.items() if val == min_value]
        most_popular_courses = self.most_popular_course()
        least_popular_courses = [course for course in least_popular_courses if course not in most_popular_courses]
        if not least_popular_courses:
            return ['n/a']
        return least_popular_courses

    def determine_course_activity(self) -> None:
        """Determine and update the student activity for each course"""
        for course in self.courses:
            total_submissions = sum(s.submissions[course] for s in self.student_manager.students)
            if total_submissions > 0:
                self.student_activity[course] = total_submissions
            else:
                self.student_activity[course] = 'n/a'
    
    def determine_valid_activities(self) -> dict:
        """Return a dictionary of courses with valid activity values"""
        return {course: value for course, value in self.student_activity.items() if value != 'n/a'}
        
    def highest_activity_course(self) -> list:
        """Find the courses with the highest student activity"""
        self.determine_course_activity()  # Ensure activity is updated
        valid_activities = self.determine_valid_activities()
        if not valid_activities:
            return ['n/a']
        max_value = max(valid_activities.values())
        highest_activity_courses = [course for course, val in valid_activities.items() if val == max_value]
        return highest_activity_courses

    def lowest_activity_course(self) -> list:
        """Find the courses with the lowest student activity"""
        self.determine_course_activity()  # Ensure activity is updated
        valid_activities = self.determine_valid_activities()
        if not valid_activities:
            return ['n/a']
        min_value = min(valid_activities.values())
        lowest_activity_courses = [course for course, val in valid_activities.items() if val == min_value]
        highest_activity_courses = self.highest_activity_course()
        lowest_activity_courses = [course for course in lowest_activity_courses if course not in highest_activity_courses]
        if not lowest_activity_courses:
            return ['n/a']
        return lowest_activity_courses

    def determine_course_difficulty(self) -> None:
        """Determine the difficulty of each course and update the self.difficulty dictionary"""
        for course in self.courses:
            total_points = sum(s.progress[course] for s in self.student_manager.students)
            total_submissions = sum(s.submissions[course] for s in self.student_manager.students)
            if total_submissions > 0:
                avg_score = total_points / total_submissions
                self.difficulty[course] = avg_score
            else:
                self.difficulty[course] = 'n/a'
                
    def determine_valid_difficulties(self) -> dict:
        """Return a dictionary of courses with valid difficulty values"""
        return {course: avg for course, avg in self.difficulty.items() if avg != 'n/a'}

    def easiest_course(self) -> list:
        """Find the courses with the highest average score per submission"""
        self.determine_course_difficulty()  # Ensure difficulty is updated
        valid_difficulties = self.determine_valid_difficulties()
        if not valid_difficulties:
            return ['n/a']
        max_avg = max(valid_difficulties.values())
        easiest_courses = [course for course, avg in valid_difficulties.items() if avg == max_avg]
        return easiest_courses
    
    def hardest_course(self) -> list:
        """Find the courses with the lowest average score per submission"""
        self.determine_course_difficulty()  # Ensure difficulty is updated
        valid_difficulties = self.determine_valid_difficulties()
        if not valid_difficulties:
            return ['n/a']
        min_avg = min(valid_difficulties.values())
        hardest_courses = [course for course, avg in valid_difficulties.items() if avg == min_avg]
        easiest_courses = self.easiest_course()
        hardest_courses = [course for course in hardest_courses if course not in easiest_courses]
        if not hardest_courses:
            return ['n/a']
        return hardest_courses
    
    def get_completion_percentage(self, course: str, points: int) -> float:
        """Calculate the percentage of completion for a course based on total points"""
        total_points_needed = {
            'Python': 600,
            'DSA' : 400,
            'Databases': 480,
            'Flask': 550
        }
        return (points / total_points_needed[course]) * 100
                
    def display_course_details(self, course: str) -> None:
        """Display the list of students with their total points"""
        print(f'{course}')
        print(f"{'id':<24} {'points':<12} {'completed':<12}")
        enrolled_students = self.determine_enrolled_students(course)
        if not enrolled_students:
            return  # No students enrolled in this course
        sorted_students = sorted(enrolled_students, key=lambda s: (-s.progress[course], s.student_id))
        for student in sorted_students:
            points = student.progress[course]
            course_completion = self.get_completion_percentage(course, points)
            print(f'{student.student_id:<24} {points:<12} {course_completion:.1f}%')
    
    def course_statistics(self) -> None:
        """Display course statistics and handle course-specific queries"""
        print("Type the name of a course to see details or 'back' to quit:")

        most_popular = self.most_popular_course()
        least_popular = self.least_popular_course()
        highest_activity = self.highest_activity_course()
        lowest_activity = self.lowest_activity_course()
        easiest_course = self.easiest_course()
        hardest_course = self.hardest_course()
        
        print(f"Most popular: {', '.join(most_popular)}")
        print(f"Least popular: {', '.join(least_popular)}")
        print(f"Highest activity: {', '.join(highest_activity)}")
        print(f"Lowest activity: {', '.join(lowest_activity)}")
        print(f"Easiest course: {', '.join(easiest_course)}")
        print(f"Hardest course: {', '.join(hardest_course)}")
        
        while True:
            user_input = input().strip().lower()
            if user_input.lower() == 'back':
                break
            matching_course = next((course for course in self.courses if course.lower() == user_input.lower()), None)
            if matching_course:
                self.display_course_details(matching_course)
            else:
                print('Unknown course')
    
    def determine_course_completion(self, course: str) -> None:
        """Determine the students who finished a course"""
        enrolled_students = self.determine_enrolled_students(course)
        for student in enrolled_students:
            if not student.completed_courses[course]:
                points = student.progress[course]
                course_completion = self.get_completion_percentage(course, points)
                if course_completion >= 100:
                    student.completed_courses[course] = True
    
    def notify_students(self) -> None:
        """Sends course completion notifications to students who completed a course"""
        notifications_sent = 0
        notified_students = set()
        
        for course in self.courses:
            self.determine_course_completion(course)
        
        for student in self.student_manager.students:
            for course in self.courses:
                if student.completed_courses[course] and not student.notifications_sent[course]:
                    print(f'To: {student.email}')
                    print('Re: Your Learning Progress')
                    full_name = f'{student.first_name} {student.last_name}'
                    print(f'Hello, {full_name}! You have accomplished our {course} course!')
                    student.notifications_sent[course] = True
                    if student.student_id not in notified_students:
                        notified_students.add(student.student_id)
                        notifications_sent += 1
        print(f"Total {notifications_sent} student{'s' if notifications_sent != 1 else ''} have been notified.")
            

def main() -> None:
    """Main function to handle the program execution."""
    print("Learning Progress Tracker")
    manager = StudentManager()
    course = CourseManager(manager)

    while True:
        user_command = input().strip().lower()

        if user_command == 'exit':
            print('Bye!')
            break
        elif user_command == 'add students':
            manager.add_students()
        elif user_command == 'list':
            manager.list_student_ids()
        elif user_command == 'add points':
            manager.add_points()
        elif user_command == 'find':
            manager.find_student()
        elif user_command == 'statistics':
            course.course_statistics()
        elif user_command == 'notify':
            course.notify_students()
        elif user_command == 'back':
            print("Enter 'exit' to exit the program.")
        elif not user_command:
            print('No input')
        else:
            print('Error: unknown command')


if __name__ == '__main__':
    main()