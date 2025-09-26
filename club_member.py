from datetime import datetime
from typing import TYPE_CHECKING

# from assignment import Assignment
# from club import Club
from database import Database
from errors import AlreadyMember, PermissionDenied
# from student import Student
# from submission import Submission

if TYPE_CHECKING:
    from assignment import Assignment
    from club import Club
    from student import Student
    from submission import Submission

db = Database()


# Manager capabilities minus the add assignments
class ClubMember:
    def __init__(self, student: 'Student', club: 'Club'):
        self.student = student
        self.club = club
        self.joined_date = datetime.now()

    def view_club_assignments(self) -> ['Assignment']:
        return self.club.view_assignments()

    def view_my_submissions(self) -> ['Submission']:
        return [s for s in self.student.get_submissions() if s.assignment.club == self.club]


# Admin capabilities minus the add/remove member
class ClubManager(ClubMember):

    def add_assignment(self, title: str, max_score: int, deadline: str) -> 'Assignment':
        assignment = Assignment(title, max_score, deadline, self.club)
        self.club.assignments.append(assignment)
        return assignment

    def remove_assignment(self, assignment: 'Assignment'):
        if assignment in self.club.assignments:
            self.club.assignments.remove(assignment)


# Admin has all permissions associated with club
class ClubAdmin(ClubManager):

    def add_member(self, student: 'Student') -> ClubMember:
        if self.club.is_member(student):
            raise AlreadyMember()
        member = self.club.add_member(student)
        student.clubs.append(self.club)
        return member

    def remove_member(self, member: ClubMember):
        if member.club != self.club:
            raise PermissionDenied()

        self.club.members.remove(member)
        member.student.clubs.remove(self.club)
