from student import Student
from assignment import Assignment
from submission import Submission
import datetime

students = []
club = []
current_user = None


def main():
    global curr_user
    print("WELCOME TO IITR CLUB MANAGEMENT SYSTEM")
    while True:
        print("Options: register, login, create_club, join_club, add_assignment")
        cmd = input("> ").strip().lower()
        if cmd == "exit":
            break


if __name__ == "__main__":
    main()
