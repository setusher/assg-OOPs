from datetime import datetime
from typing import TypeVar

from club_member import ClubManager, ClubMember
from database import Database
from errors import PermissionDenied
from submission import Submission

T = TypeVar('T')
db = Database()


class Assignment:
    def __init__(self: T, title: str, max_score: int, deadline: datetime, club: 'Club', publisher: 'ClubManager'):
        from vector import Vector

        self.title: str = title
        self.max_score: int = max_score
        self.deadline: datetime = deadline
        self.club: 'Club' = club
        self.submissions: Vector['Submissions'] = Vector()
        self.publisher: 'ClubManager' = publisher

    def submit_assignment(self, student: 'Student', content: str) -> 'Submission':
        s = Submission(student, self, content)
        self.submissions.append(s)
        return s

    def view_submissions(self) -> list['Submission']:
        from session import Session
        session = Session()
        mem = self.club.get_member(session.current_user)
        if mem is None:
            raise PermissionDenied()
        elif isinstance(mem, ClubMember):
            return [x for x in self.submissions if x.student == session.current_user].copy()
        else:
            return self.submissions.copy()

    def is_late(self, submission_date: datetime) -> bool:
        return submission_date > self.deadline
