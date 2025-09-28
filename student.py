from typing import TypeVar

from club import Club
from database import Database
from errors import BadFormatException, InvalidPassword

T = TypeVar('T')

db = Database()


class Student:
    def __init__(self: T, enrollment: str, name: str, password: str):
        self.enrollment = enrollment
        self.name = name
        self.password = password

    def register(self) -> T:
        if len(self.name) < 1 or len(self.enrollment) != 8 or not self.enrollment.isdigit():
            raise BadFormatException("Invalid name or enrollment number!")

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
        c = []
        for club in db.get_clubs():
            students = []
            for m in club.get_members():
                students.append(m.student)
            if self in students:
                c.append(club)
        return c

    def get_assignments(self) -> list['Assignment']:
        assignments = []
        for x in self.get_clubs():
            assignments.extend(x.get_assignments())
        return assignments

    def get_submissions(self) -> list['Submission']:
        sub = []
        for a in self.get_assignments():
            sub.extend(a.submissions)
        return sub

    def create_club(self, name: str):
        if any(x.name == name for x in db.get_clubs()):
            raise BadFormatException("Club with same name already exists!")

        club = Club(name, self)
        db.add_club(club)

    def __eq__(self, other):
        if isinstance(other, Student):
            return self.enrollment == other.enrollment
        return NotImplemented
