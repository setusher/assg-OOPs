class BadFormatException(Exception):
    pass

class InvalidPassword(BadFormatException):
    def __init__(self):
        super().__init__("Password must be 8 characters long!")


class AlreadyMember(Exception):
    def __init__(self):
        super().__init__("User already member of the club!")
