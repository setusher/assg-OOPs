from errors import BadFormatException, InvalidPassword
from typing import TypeVar
import datetime
from student import Student
from club import Club

T = TypeVar('T')


class Assignment:
    def __init__(self, title: str, max_score: int, deadline: str, club):
        self.title = title
        self.max_score = max_score
        self.deadline = deadline
        self.club = club
        # submissions


    def is_late(self, submission_date: datetime) -> bool:
        return submission_date > self.deadline