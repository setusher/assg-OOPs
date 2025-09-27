from typing import TypeVar
from database import Database
from errors import BadFormatException, InvalidPassword

T = TypeVar('T')

db = Database()


class Student:
    def __init__(self: T, enrollment: str, name: str, password: str):
        self.enrollment = enrollment
        self.name = name
        self.clubs = []
        self.password = password

    def register(self) -> T:
        if len(self.name) < 1 or len(self.enrollment) != 8:
            raise BadFormatException()

        if len(self.password) < 8:
            raise InvalidPassword()

        if db.get_student(self.enrollment):
            raise BadFormatException("Student with this enrollment already exists")

        db.add_student(self)
        return self

    @staticmethod
    def login(enrollment: str, password: str):
        student = db.get_student(enrollment)
        if student and student.password == password:
            return student
        raise BadFormatException("Invalid credentials!")

    def get_clubs(self) -> list['Club']:
        return self.clubs.copy()

    def get_assignments(self) -> list['Assignment']:
        assignments = [x for x in db.assignments if x.club in self.clubs]
        return assignments.copy()

    def get_submissions(self) -> list['Submission']:
        sub = [x for x in db.submissions if x.student == self]
        return sub.copy()
