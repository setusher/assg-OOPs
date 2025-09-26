from datetime import datetime
from typing import TypeVar

# from club import Club
# from submission import Submission

T = TypeVar('T')


class Assignment:
    def __init__(self: T, title: str, max_score: int, deadline: datetime, club: 'Club'):
        self.title: str = title
        self.max_score: int = max_score
        self.deadline: datetime = deadline
        self.club: 'Club' = club
        self.submissions: list['Submission'] = []

    def submit_assignment(self, assignment: T, content: str) -> 'Submission':
        pass

    def view_submissions(self):
        pass

    def is_late(self, submission_date: datetime) -> bool:
        return submission_date > self.deadline
