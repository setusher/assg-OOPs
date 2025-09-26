from typing import TypeVar, Optional, List, Dict

# from assignment import Assignment
# from club import Club
# from student import Student
# from submission import Submission

T = TypeVar('T')


class DatabaseMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Database(metaclass=DatabaseMeta):
    def __init__(self):
        self.students: Dict[str, 'Student'] = {}  # key is enrollment
        self.clubs: List['Club'] = []
        self.assignments: List['Assignment'] = []
        self.submissions: List['Submission'] = []

    def add_student(self, student: 'Student'):
        self.students[student.enrollment] = student

    def get_student(self, enrollment: str) -> Optional['Student']:
        return self.students.get(enrollment)

    def add_club(self, club: 'Club'):
        self.clubs.append(club)

    def get_clubs(self) -> List['Club']:
        return self.clubs.copy()
