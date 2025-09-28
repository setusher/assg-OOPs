from datetime import datetime
from typing import TYPE_CHECKING

from database import Database

if TYPE_CHECKING:
    from assignment import Assignment
    from club import Club
    from student import Student
    from submission import Submission

db = Database()


# Manager capabilities minus the add assignments
class ClubMember:
    def __init__(self, student: 'Student', club: 'Club'):
        from vector import Vector
        self.student = student
        self.club = club
        self.joined_date = datetime.now()

    def view_club_assignments(self) -> Vector['Assignment']:
        return self.club.view_assignments()

    def view_my_submissions(self) -> Vector['Submission']:
        return [s for s in self.student.get_submissions() if s.assignment.club == self.club]


# Admin capabilities minus the add/remove member
class ClubManager(ClubMember):

    def add_assignment(self, title: str, max_score: int, deadline: datetime) -> 'Assignment':
        assignment = Assignment(title, max_score, deadline, self.club, self)
        self.club.add_assignment(assignment)
        return assignment

    def remove_assignment(self, assignment: 'Assignment'):
        self.club.remove_assignment(assignment)


# Admin has all permissions associated with club
class ClubAdmin(ClubManager):

    def add_member(self, student: 'Student') -> ClubMember:
        member = self.club.add_member(student)
        return member

    def remove_member(self, student: 'Student'):
        self.club.remove_member(student)

    def promote_member(self, member):
        from errors import BadFormatException, NotMember
        if member not in self.club.get_members():
            raise NotMember()

        target_index = self.club.get_members().index(member)

        if isinstance(self.club.get_members()[target_index], (ClubManager, ClubAdmin)):
            raise BadFormatException("The member is already a manager/admin!")

        promoted = ClubManager(member.student, self.club)
        self.club.promote_member_status(promoted, target_index)
        return promoted
