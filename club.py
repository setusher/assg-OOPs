from assignment import Assignment
from club_member import ClubAdmin, ClubMember
from database import Database
from errors import AlreadyMember, NotMember
from student import Student

db = Database()


class Club:
    def __init__(self, name: str, admin: Student, assignments: list[Assignment] = None):
        self.name = name
        self.admin: Student = admin
        self.members: list[ClubMember] = []
        self.assignments: list[Assignment] = assignments or []

        admin_m = ClubAdmin(admin, self)
        self.members.append(admin_m)
        admin.clubs.append(self)

        db.add_club(self)

    def add_member(self, student: Student) -> ClubMember:
        if self.is_member(student):
            raise AlreadyMember()
        member = ClubMember(student, self)
        self.members.append(member)
        return member

    def remove_member(self, student: Student):
        to_rem = None
        for m in self.members:
            if m.student == student:
                to_rem = m
                break

        if to_rem:
            self.members.remove(to_rem)
        else:
            raise NotMember()

    def list_members(self):
        return self.members

    def view_assignments(self):
        return self.assignments.copy()

    def is_member(self, student: Student) -> bool:
        return any(m.student == student for m in self.members)
