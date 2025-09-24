class ClubRole:
    def __init__(self, title: str):
        self.title = title


# Admin has all permissions associated with club
class ClubAdmin(ClubRole):
    def __init__(self):
        super().__init__("Admin")


# Admin capabilities minus the add/remove member
class ClubManager(ClubRole):
    def __init__(self):
        super().__init__("Manager")


# Manager capabilities minus the add assignments
class ClubMember(ClubRole):
    def __init__(self):
        super().__init__("Member")
