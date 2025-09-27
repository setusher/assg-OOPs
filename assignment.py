from datetime import datetime
from typing import TypeVar

from club_member import ClubManager
from database import Database
from submission import Submission

T = TypeVar('T')
db = Database()


class Assignment:
    def __init__(self: T, title: str, max_score: int, deadline: datetime, club: 'Club', publisher: 'ClubManager'):
        self.title: str = title
        self.max_score: int = max_score
        self.deadline: datetime = deadline
        self.club: 'Club' = club
        self.submissions: list['Submission'] = []
        self.publisher: 'ClubManager' = publisher

    def submit_assignment(self, student: 'Student', assignment: T, content: str) -> 'Submission':
        s = Submission(student, assignment, content)
        self.submissions.append(s)
        return s

    def view_submissions(self) -> list['Submission']:
        return self.submissions.copy()
        # TODO This should be based on current user -
        #  if manager then return all otherwise only of that user's own

    def is_late(self, submission_date: datetime) -> bool:
        return submission_date > self.deadline
