from errors import BadFormatException, InvalidPassword
from typing import TypeVar
from student import Student


T = TypeVar('T')

class Club: 
    def __init__(self, name, admin):
        self.name = name
        self.admin = admin
        self.members = [admin]
        #assignments

    def list_members(self):
        print(f"Members of {self.name}:")
        for member in self.members:
            print(f"  {member.name} ({member.enrollment})")

    def view_assignments(self):
        print(f"Assignments of {self.name}:")
        for assignment in self.assignments:
            print(f"  {assignment.title}, Max Score: {assignment.max_score}, Deadline: {assignment.deadline}")

