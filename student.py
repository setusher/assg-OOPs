from errors import BadFormatException, InvalidPassword
from typing import TypeVar
from club import Club

T = TypeVar('T')


class Student:
    def __init__(self: T, enrollment: str, name: str, password: str):
        self.enrollment = enrollment
        self.name = name
        self.clubs = []
        

    def register(self) -> T:
        if len(self.name) < 1 or len(self.enrollment) != 8:
            raise BadFormatException

        if len(self.password) < 8:
            raise InvalidPassword

        # do ops to register this user and return student obj

    @staticmethod
    def login(enrollment: str, password: str, student_list: list):
        for student in student_list:
            if student.enrollment == enrollment and student.password == password:
                print("Login successful!")
                return student
        print("Login failed!")
        return None

    def join_club(self, club: 'Club'):
        if club not in self.clubs:
            self.clubs.append(club)
            club.add_member(self)
            print(f"{self.name} joined {club.name}")
        else:
            print(f"{self.name} is already a member of {club.name}")

    def get_clubs(self):
        if self.clubs:
            print(f"{self.name} is a member of these clubs:")
            for club in self.clubs:
                print("-", club.name)
        else:
            print(f"{self.name} is not a member of any club.")
