from datetime import datetime
from typing import Optional

# from assignment import Assignment
# from student import Student


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
        self.score = score
        self.feedback = feedback
        self.graded_by = grader

    def is_late(self) -> bool:
        return self.assignment.is_late(self.submission_date)
