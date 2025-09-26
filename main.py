from student import Student
from club import Club
from assignment import Assignment
from submission import Submission
from errors import BadFormatException, InvalidPassword, AlreadyMember
import datetime

students = []
clubs = []
current_user = None

def find_student(enrollment):
    for student in students:
        if student.enrollment == enrollment:
            return student
    return None

def find_club(name):
    for club in clubs:
        if club.name == name:
            return club
    return None

def display_menu(options, header="Choose an option:"):
    print("\n" + "="*len(header))
    print(header)
    print("="*len(header))
    for idx, opt in enumerate(options, 1):
        print(f"[{idx}] {opt}")
    print()

def get_choice(num_choices):
    while True:
        try:
            choice = int(input("Enter choice: "))
            if 1 <= choice <= num_choices:
                return choice
            else:
                print(f"Invalid choice! Please enter a number between 1 and {num_choices}.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def list_students():
    if not students:
        print("No registered students yet.")
        return
    print("\nRegistered students:")
    for s in students:
        print(f"- {s.name} ({s.enrollment})")

def list_clubs():
    if not clubs:
        print("No clubs created yet.")
        return
    print("\nClubs:")
    for c in clubs:
        print(f"- {c.name} (Admin: {c.admin.name}) Members: {len(c.members)} Assignments: {len(c.assignments)}")

def user_club_menu():
    joined = [club for club in clubs if current_user in club.members]
    if not joined:
        print("You are not a member of any club yet.")
        return
    display_menu([club.name for club in joined], "Your Clubs")
    ch = get_choice(len(joined))
    return joined[ch-1]

def main():
    global current_user
    print("WELCOME TO IITR CLUB MANAGEMENT SYSTEM")
    while True:
        print("\n--- MAIN MENU ---")
        options = [
            "Register as Student", "Login", "List Students", "List Clubs",
            "Create Club", "Join Club", "View My Clubs", "Add Assignment (Admin)",
            "View Assignments (Member)", "Submit Assignment", "Logout", "Exit"
        ]
        display_menu(options)
        choice = get_choice(len(options))

        if choice == 1:  # Register
            enrollment = input("Enrollment number: ").strip()
            name = input("Name: ").strip()
            password = input("Password (min 8 chars): ").strip()
            try:
                student = Student(enrollment, name, password)
                student.register()
                students.append(student)
                print("Registration successful.")
            except (BadFormatException, InvalidPassword) as e:
                print("Registration failed:", e)

        elif choice == 2:  # Login
            enrollment = input("Enrollment number: ").strip()
            password = input("Password: ").strip()
            student = find_student(enrollment)
            if student and student.password == password:
                current_user = student
                print(f"Login successful. Welcome, {student.name}!")
            else:
                print("Login failed. Check enrollment and password.")

        elif choice == 3:  # List Students
            list_students()

        elif choice == 4:  # List Clubs
            list_clubs()

        elif choice == 5:  # Create Club
            if not current_user:
                print("Please login first.")
                continue
            name = input("Club name: ").strip()
            club = find_club(name)
            if club:
                print("Club already exists.")
            else:
                club = Club(name, current_user)
                clubs.append(club)
                print(f"Club '{name}' created. You are the admin.")

        elif choice == 6:  # Join Club
            if not current_user:
                print("Please login first.")
                continue
            if not clubs:
                print("No clubs to join. Create a club first!")
                continue
            display_menu([club.name for club in clubs], "Available Clubs")
            join_idx = get_choice(len(clubs))
            club = clubs[join_idx-1]
            try:
                current_user.join_club(club)
                print(f"{current_user.name} joined {club.name}.")
            except AlreadyMemberException as e:
                print(e)

        elif choice == 7:  # View My Clubs
            if not current_user:
                print("Please login first.")
                continue
            if not current_user.clubs:
                print("You haven't joined any clubs.")
            else:
                print("\nYour clubs:")
                for club in current_user.clubs:
                    print(f"- {club.name}")

        elif choice == 8:  # Add Assignment (Admin)
            if not current_user:
                print("Please login first.")
                continue
            admin_clubs = [club for club in clubs if club.admin == current_user]
            if not admin_clubs:
                print("You are not admin of any club.")
                continue
            display_menu([club.name for club in admin_clubs], "Your Admin Clubs")
            ch = get_choice(len(admin_clubs))
            club = admin_clubs[ch-1]
            title = input("Assignment title: ").strip()
            maxscore = int(input("Max Score: "))
            deadline = input("Deadline (YYYY-MM-DD): ").strip()
            deadline_dt = datetime.datetime.strptime(deadline, "%Y-%m-%d")
            assignment = Assignment(title, maxscore, deadline_dt, club)
            club.assignments.append(assignment)
            print(f"Assignment '{title}' added to {club.name}.")

        elif choice == 9:  # View Assignments (Member)
            if not current_user:
                print("Please login first.")
                continue
            club = user_club_menu()
            if club and club.assignments:
                print(f"\nAssignments for {club.name}:")
                for a in club.assignments:
                    print(f"- {a.title} (Max: {a.maxscore}, Deadline: {a.deadline})")
            else:
                print("No assignments for this club.")

        elif choice == 10:  # Submit Assignment
            if not current_user:
                print("Please login first.")
                continue
            club = user_club_menu()
            if not club:
                continue
            if not club.assignments:
                print("No assignments to submit in this club.")
                continue
            display_menu([a.title for a in club.assignments], "Assignments")
            ch = get_choice(len(club.assignments))
            assignment = club.assignments[ch-1]
            score = int(input("Enter your score: "))
            sub_date_str = input("Submission Date (YYYY-MM-DD): ").strip()
            sub_date = datetime.datetime.strptime(sub_date_str, "%Y-%m-%d")
            submission = Submission(current_user, assignment, sub_date, score)
            assignment.submissions[current_user] = submission
            print(f"Assignment '{assignment.title}' submitted.")

        elif choice == 11:  # Logout
            current_user = None
            print("Logged out.")

        elif choice == 12:  # Exit
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
