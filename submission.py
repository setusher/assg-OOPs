from student import Student

class Submission:
    def __init__(self, student: Student, assignment: Assignment, submission_date: datetime, score: int):
        self.student = student
        self.assignment = assignment
        self.submission_date = submission_date
        self.score = score

    def is_late(self, submission_date: datetime) -> bool:
        return submission_date > self.assignment.deadline

    def mark_late(self):
        pass