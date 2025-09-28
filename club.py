from typing import Optional

from assignment import Assignment
from club_member import ClubMember
from database import Database
from errors import NotMember

db = Database()


class Club:
    def __init__(self, name: str, admin: 'Student', assignments: list['Assignment'] = None):
        self.name = name
        self.admin: 'ClubAdmin' = admin
        self.members: list['ClubMember'] = []
        self.assignments: list['Assignment'] = assignments or []

        from club_member import ClubAdmin, ClubMember

        admin_m = ClubAdmin(admin, self)
        self.members.append(admin_m)

    def add_member(self, student: 'Student') -> 'ClubMember':
        from club_member import ClubMember
        from errors import AlreadyMember

        if self.is_member(student):
            raise AlreadyMember()

        member = ClubMember(student, self)
        self.members.append(member)
        return member

    def remove_member(self, student: 'Student'):
        to_rem = None
        for m in self.members:
            if m.student == student:
                to_rem = m
                break
        if to_rem:
            self.members.remove(to_rem)
        else:
            raise NotMember()

    def add_assignment(self, assignment: 'Assignment'):
        self.assignments.append(assignment)

    def view_assignments(self):
        return self.assignments.copy()

    def remove_assignment(self, assignment: 'Assignment'):
        try:
            self.assignments.remove(assignment)
        except ValueError:
            pass

    def is_member(self, student: 'Student') -> bool:
        return self.get_member(student) is not None

    def get_member(self, student: 'Student') -> Optional['ClubMember']:
        for m in self.members:
            if m.student == student:
                return m
        return None

    def __eq__(self, other):
        if isinstance(other, Club):
            return self.name == other.name
        return NotImplemented
