from typing import TypeVar

from assignment import Assignment
from club import Club
from club_member import ClubMember
from database import Database
from errors import BadFormatException, InvalidPassword, AlreadyMember, NotMember
from submission import Submission

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
        return None

    def join_club(self, club: Club) -> ClubMember:
        if club in self.clubs:
            raise AlreadyMember()

        self.clubs.append(club)
        member = club.add_member(self)
        return member

    def leave_club(self, club: Club):
        if club not in self.clubs:
            raise NotMember()

        self.clubs.remove(club)
        club.remove_member(self)

    def get_clubs(self) -> [Club]:
        return self.clubs.copy()

    def get_assignments(self):
        pass

    def submit_assignment(self, assignment: Assignment) -> Submission:
        pass

    def get_submissions(self) -> [Submission]:
        pass
