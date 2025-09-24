from typing import TypeVar

from club import Club
from club_member import ClubMember
from errors import BadFormatException, InvalidPassword, AlreadyMember

T = TypeVar('T')


class Student:
    def __init__(self: T, enrollment: str, name: str, password: str):
        self.enrollment = enrollment
        self.name = name
        self.clubs = []
        self.password = password

    def register(self) -> T:
        if len(self.name) < 1 or len(self.enrollment) != 8:
            raise BadFormatException

        if len(self.password) < 8:
            raise InvalidPassword
        # do ops to register this user and return student obj

    @staticmethod
    def login(enrollment: str, password: str):
        pass

    def join_club(self, club: 'Club') -> ClubMember:
        if club not in self.clubs:
            self.clubs.append(club)
            club.add_member(self)
            # create a club member in singleton and then return it here
        else:
            raise AlreadyMember

    def get_clubs(self):
        return self.clubs
