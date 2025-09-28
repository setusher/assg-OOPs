from typing import TypeVar, Optional, List, Dict

T = TypeVar('T')


class DatabaseMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Database(metaclass=DatabaseMeta):
    
    def __init__(self):
        from vector import Vector
        self.students: Dict[str, 'Student'] = {}  # key is enrollment
        self.clubs: Vector['Club'] = Vector()
        self.assignments: Vector['Assignment'] = Vector()
        self.submissions: Vector['Submission'] = Vector()

    def add_student(self, student: 'Student'):
        self.students[student.enrollment] = student

    def get_student(self, enrollment: str) -> Optional['Student']:
        return self.students.get(enrollment)

    def get_students(self) -> list['Students']:
        return self.students.copy()

    def update_student(self, student: 'Student'):
        self.students[student.enrollment] = student

    def add_club(self, club: 'Club'):
        self.clubs.append(club)

    def get_clubs(self) -> list['Club']:
        return self.clubs.copy()

    def add_submission(self, submission: 'Submission') -> None:
        
        self.submissions.append(submission)

    def get_submissions(self):
        try:
            return self.submissions.copy()
        except Exception:
            return self.submissions
