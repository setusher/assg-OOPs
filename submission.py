from datetime import datetime
from typing import Optional

from errors import PermissionDenied


class Submission:
    def __init__(self, student: 'Student', assignment: 'Assignment', content: str,
                 submission_date: datetime = None):
        self.student = student
        self.assignment = assignment
        self.content = content
        self.submission_date = submission_date or datetime.now()
        self.score: Optional[int] = None
        self.feedback: str = ""
        self.graded_by: Optional['Student'] = None

    def grade(self, grader: 'Student', score: int, feedback: str = ""):
        if score < 0 or score > self.assignment.max_score:
            raise ValueError(f"Score must be between 0 and {self.assignment.max_score}")
        if grader is None:
            raise ValueError("Grader must be provided when grading a submission")
        if grader != self.assignment.publisher:
            raise PermissionDenied()
        self.score = score
        self.feedback = feedback
        self.graded_by = grader

    def is_late(self) -> bool:
        return self.assignment.is_late(self.submission_date)

    def __eq__(self, other):
        if isinstance(other, Submission):
            return self.student == other.student and self.assignment == other.assignment
        return NotImplemented
