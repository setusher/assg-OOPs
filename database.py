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

    def add_student(self, student: 'Student'):
        self.students[student.enrollment] = student

    def get_student(self, enrollment: str) -> Optional['Student']:
        return self.students.get(enrollment)

    def get_students(self) -> list['Students']:
        return list(self.students.values())

    def update_student(self, student: 'Student'):
        self.students[student.enrollment] = student

    def add_club(self, club: 'Club'):
        if any(c is club or c.name == club.name for c in self.clubs):
            return
        self.clubs.append(club)

    def get_clubs(self) -> List['Club']:
        return self.clubs.copy()
