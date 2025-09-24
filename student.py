from errors import BadFormatException, InvalidPassword
from typing import TypeVar

T = TypeVar('T')


class Student:
    def __init__(self: T, enrollment: str, name: str, password: str):
        self.enrollment = enrollment
        self.name = name
        self.password = password
        # clubs =

    def register(self) -> T:
        if len(self.name) < 1 or len(self.enrollment) != 8:
            raise BadFormatException

        if len(self.password) < 8:
            raise InvalidPassword

        # do ops to register this user and return student obj

    @staticmethod
    def login(enrollment: str, password: str) -> T:
        pass
        # do op to login and get the student obj

    def join_club(self):
        pass
        # get club as argument and then create a new Member obj with this student
        # and that particular club attached

    def get_clubs(self):
        pass
        # get the associated member classes of the student and then get the clubs
