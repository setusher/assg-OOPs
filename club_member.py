# Manager capabilities minus the add assignments
class ClubMember:
    pass


# Admin capabilities minus the add/remove member
class ClubManager(ClubMember):
    pass


# Admin has all permissions associated with club
class ClubAdmin(ClubManager):
    pass
