class BadFormatException(Exception):
    pass


class InvalidPassword(BadFormatException):
    def __init__(self):
        super().__init__("Password must be 8 characters long!")


class AlreadyMember(Exception):
    def __init__(self):
        super().__init__("User already member of the club!")


class NotMember(Exception):
    def __init__(self):
        super().__init__("User is not a member of this club!")


class PermissionDenied(Exception):
    def __init__(self):
        super().__init__("You don't have permission to perform this action!")


class NoUserLoggedIn(Exception):
    def __init__(self):
        super().__init__("No user is logged in!")
