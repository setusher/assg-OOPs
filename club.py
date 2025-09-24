from typing import TypeVar

from assignment import Assignment
from student import Student

T = TypeVar('T')


class Club:
    def __init__(self, name: str, admin: Student, assignments: list[Assignment] = None):
        self.name = name
        self.admin = admin
        self.members = [admin]
        self.assignments = assignments

    def list_members(self):
        return self.members

    def view_assignments(self):
        return self.assignments
