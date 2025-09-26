import datetime
from typing import TypeVar

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