from typing import Optional

from errors import NoUserLoggedIn
from student import Student


class SessionMeta(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Session(metaclass=SessionMeta):
    def __init__(self):
        self.current_user: Optional['Student'] = None
        self.is_logged_in: bool = False

    def login(self, enrollment: str, password: str):
        student = Student.login(enrollment, password)
        if student:
            self.current_user = student
            self.is_logged_in = True
            return student
        return None

    def logout(self):
        if self.is_logged_in:
            self.current_user = None
            self.is_logged_in = False
        else:
            raise NoUserLoggedIn()

    def get_current_user(self) -> Optional['Student']:
        return self.current_user if self.is_logged_in else None
