class BadFormatException(Exception):
    pass

class InvalidPassword(BadFormatException):
    pass


class AlreadyMember(Exception):
    def __init__(self):
        super().__init__("User already member of the club!")
