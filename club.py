from typing import TypeVar

from assignment import Assignment
from club_member import ClubAdmin, ClubMember
from database import Database
from student import Student

T = TypeVar('T')

db = Database()


class Club:
    def __init__(self, name: str, admin: Student, assignments: list[Assignment] = None):
        self.name = name
        self.admin: Student = admin
        self.members: [Student] = []
        self.assignments: [Assignment] = assignments or []

        admin_m = ClubAdmin()
        self.members.append(admin_m)
        admin.clubs.append(self)

        db.add_club(self)

    def add_member(self, student: Student) -> ClubMember:
        pass

    def remove_member(self, student: Student):
        pass

    def list_members(self):
        return self.members

    def view_assignments(self):
        return self.assignments

    def is_member(self, student: Student) -> bool:
        pass
