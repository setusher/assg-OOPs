from datetime import datetime

import inquirer
import typer

from database import Database
from errors import BadFormatException, InvalidPassword
from session import Session
from student import Student

app = typer.Typer(help="Student Management System")
db = Database()
session = Session()


def select_option(options, message):
    questions = [inquirer.List('choice', message=message, choices=options)]
    answers = inquirer.prompt(questions)
    return answers['choice'] if answers else None


@app.command()
def main_menu():
    options = ["Register", "Login", "Exit"]
    while True:
        typer.echo("\n" + "=" * 50)
        typer.secho("🎓 Student Management System", fg=typer.colors.CYAN, bold=True)
        typer.echo("=" * 50)

        choice = select_option(options, "What would you like to choose?")

        if choice == "Register":
            handle_register()
        elif choice == "Login":
            handle_login()
        elif choice == "Exit":
            typer.secho("\n👋 Thank you for using Student Management System!",
                        fg=typer.colors.GREEN, bold=True)
            break
        elif choice is None:
            typer.secho("\n👋 Goodbye!", fg=typer.colors.YELLOW)
            break


def handle_register():
    typer.echo("\n" + "=" * 30)
    typer.secho("📝 Student Registration", fg=typer.colors.BLUE, bold=True)
    typer.echo("=" * 30)

    name = typer.prompt("Enter your full name").strip()
    enrollment = typer.prompt("Enter enrollment number (8 digits)").strip()
    password = typer.prompt("🔒 Enter password (min 8 chars)", hide_input=True)

    student = Student(name=name, enrollment=enrollment, password=password)

    try:
        result = student.register()
        typer.secho("\n🎉 Registration successful!", fg=typer.colors.GREEN, bold=True)
        session.login(result.enrollment, result.password)
        typer.secho(f"Welcome {result.name}! You are now logged in!", fg=typer.colors.CYAN)
        show_dashboard()
    except InvalidPassword as e:
        typer.secho(f"\n❌ Registration failed: {e}", fg=typer.colors.RED, bold=True)
    except BadFormatException as e:
        typer.secho(f"\n❌ Registration failed: {e}", fg=typer.colors.RED, bold=True)


def handle_login():
    typer.echo("\n" + "=" * 30)
    typer.secho("📝 Student Login", fg=typer.colors.BLUE, bold=True)
    typer.echo("=" * 30)

    enrollment = typer.prompt("Enrollment number").strip()
    password = typer.prompt("🔒 Password", hide_input=True)

    student = session.login(enrollment, password)

    if student:
        typer.secho(f"\n🎉 Welcome back {student.name}!", fg=typer.colors.GREEN, bold=True)
        show_dashboard()
    else:
        typer.secho("\n❌ Login failed! Invalid enrollment or password.", fg=typer.colors.RED, bold=True)


def show_dashboard():
    dashboard_options = ["All Clubs", "My Clubs", "My Assignments", "My Submissions", "Create Club", "Logout"]
    while True:
        while True:
            typer.echo("\n" + "=" * 50)
            typer.secho("Student Dashboard", fg=typer.colors.CYAN, bold=True)
            typer.echo("=" * 50)

            choice = select_option(dashboard_options, "What would you like to choose?")

            if choice == "All Clubs":
                show_all_clubs()
            elif choice == "My Clubs":
                show_my_clubs()
            elif choice == "My Assignments":
                show_my_assgs()
            elif choice == "My Submissions":
                show_my_subs()
            elif choice == "Create Club":
                create_club()
            elif choice == "Logout":
                session.logout()
                typer.secho("👋 Logged out successfully.", fg=typer.colors.YELLOW)
                return


def show_all_clubs():
    clubs = db.get_clubs()
    if not clubs:
        typer.secho("\n📌 No clubs available yet!", fg=typer.colors.MAGENTA)
        return

    typer.secho("\n📋 Available Clubs:", fg=typer.colors.BLUE, bold=True)
    for c in clubs:
        typer.echo(f"- {c.name}")


def show_my_clubs():
    user_clubs = session.current_user.get_clubs()

    if not user_clubs:
        typer.secho("\n📌 You are not part of any clubs yet.", fg=typer.colors.MAGENTA)
        return

    typer.secho("\n📋 My Clubs:", fg=typer.colors.BLUE, bold=True)
    club_names = [c.name for c in user_clubs]
    selected_club_name = select_option(club_names + ["Back"], "Select a club: ")

    if selected_club_name == "Back" or selected_club_name is None:
        return

    selected_club = next((c for c in user_clubs if c.name == selected_club_name), None)

    show_club_menu(selected_club)


def show_my_assgs():
    student = session.get_current_user()
    assignments = student.get_assignments()

    if not assignments:
        typer.secho("\n📌 No assignments yet.", fg=typer.colors.MAGENTA)
        return

    typer.secho("\n📋 My Assignments:", fg=typer.colors.BLUE, bold=True)
    for a in assignments:
        status = "✅ Done" if any(s.assignment == a for s in student.get_submissions()) else "❌ Pending"
        typer.echo(f"- {a.title} | Max Score: {a.max_score} | Deadline: {a.deadline} | {status}")


def show_my_subs():
    student = session.get_current_user()
    submissions = student.get_submissions()

    if not submissions:
        typer.secho("\n📌 No submissions yet.", fg=typer.colors.MAGENTA)
        return
    typer.secho("\n📋 My Submissions:", fg=typer.colors.BLUE, bold=True)
    for s in submissions:
        typer.echo(
            f"- {s.assignment.title} | Score: {s.score if s.score is None else 'Not Graded'} | Feedback: {s.feedback or 'N/A'}"
        )


def create_club():
    typer.echo("\n" + "=" * 30)
    typer.secho("📝 Create Club", fg=typer.colors.BLUE, bold=True)
    typer.echo("=" * 30)
    name = typer.prompt("Enter club name").strip()
    try:
        session.current_user.create_club(name)
    except BadFormatException as e:
        typer.secho(f"❌ {e}", fg=typer.colors.RED)

    typer.secho(f"✅ Club '{name}' created successfully! You are the admin.", fg=typer.colors.GREEN)


def show_club_menu(club):
    from club_member import ClubAdmin, ClubManager

    student = session.get_current_user()
    member = club.get_member(student)

    if member is None:
        typer.secho("❌ You are not a member of this club.", fg=typer.colors.RED)
        return

    options = ["View Assignments", "View Submissions", "View members"]
    if isinstance(member, ClubManager):
        options += ["Add Assignment", "Remove Assignment"]
    if isinstance(member, ClubAdmin):
        options += ["Add Member", "Remove Member", "Promote Member"]

    options.append("Back")

    # options = ["View Assignments", "View Submissions", "Back"]

    while True:
        typer.secho(f"\n🏛️  Club: {club.name}", fg=typer.colors.CYAN, bold=True)
        choice = select_option(options, "Choose an action:")

        if choice == "View Assignments":
            assignments = member.view_club_assignments()
            if not assignments:
                typer.secho("📌 No assignments yet.", fg=typer.colors.MAGENTA)
                continue

            assignment_titles = [a.title for a in assignments]
            selected_title = select_option(assignment_titles + ["Back"], "Select an assignment:")

            if selected_title == "Back" or selected_title is None:
                continue

            selected_assignment = next(a for a in assignments if a.title == selected_title)

            while True:
                typer.secho(f"\n Assignment: {selected_assignment.title}", fg=typer.colors.BLUE, bold=True)
                sub_options = ["Submit Assignment", "Back"]
                sub_choice = select_option(sub_options, "Choose an action:")

                if sub_choice == "Submit Assignment":

                    content = typer.prompt("Enter your submission text")
                    student = session.get_current_user()
                    selected_assignment.submit_assignment(student, content=content)

                    typer.secho("✅ Submission added successfully!", fg=typer.colors.GREEN)
                    break

                elif sub_choice == "Back" or sub_choice is None:
                    break

        elif choice == "View My Submissions":
            submissions = []

            member = club.get_member(session.get_current_user())
            if member:
                submissions.extend(member.view_my_submissions())

            if not submissions:
                typer.secho("📌 No submissions yet.", fg=typer.colors.MAGENTA)
            else:
                typer.secho("\n📋 Submissions:", fg=typer.colors.BLUE, bold=True)
                for s in submissions:
                    typer.echo(
                        f"- {s.assignment.title} | Score: {s.score if s.score is not None else 'Not graded'} | Feedback: {s.feedback or 'N/A'}"
                    )

        elif choice == "View members":
            if not club.get_members():
                typer.secho("📌 No members in this club yet.", fg=typer.colors.MAGENTA)
                continue

            typer.secho("\n📋 Club Members:", fg=typer.colors.BLUE, bold=True)
            for m in club.get_members():
                role = ""
                from club_member import ClubAdmin, ClubManager
                if isinstance(m, ClubAdmin):
                    role = typer.style("(Admin)", fg=typer.colors.RED, bold=True)
                elif isinstance(m, ClubManager):
                    role = typer.style("(Manager)", fg=typer.colors.YELLOW, bold=True)

                typer.echo(f"- {m.student.name} {role}")

        elif choice == "Add Assignment" and isinstance(member, (ClubManager, ClubAdmin)):
            title = typer.prompt("Assignment title")
            max_score = int(typer.prompt("Max score"))
            deadline_str = typer.prompt("Deadline (YYYY-MM-DD HH:MM)")
            deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M")
            member.add_assignment(title, max_score, deadline)
            typer.secho("✅ Assignment added successfully!", fg=typer.colors.GREEN)

        elif choice == "Remove Assignment" and isinstance(member, (ClubManager, ClubAdmin)):
            assignments = member.view_club_assignments()
            if not assignments:
                typer.secho("📌 No assignments to remove.", fg=typer.colors.MAGENTA)
                continue

            assignment_titles = [a.title for a in assignments]
            selected_title = select_option(assignment_titles + ["Back"], "Select assignment to remove:")
            if selected_title == "Back" or selected_title is None:
                continue

            selected_assignment = next(a for a in assignments if a.title == selected_title)
            member.remove_assignment(selected_assignment)
            typer.secho("✅ Assignment removed successfully!", fg=typer.colors.GREEN)

        elif choice == "Add Member" and isinstance(member, ClubAdmin):
            student_enrollment = typer.prompt("Enter enrollment number of the student to add")
            from student import Student
            from errors import AlreadyMember
            student = db.get_student(student_enrollment)
            if student:
                try:
                    member.add_member(student)
                    typer.secho(f"✅ {student.name} added to the club.", fg=typer.colors.GREEN)
                except AlreadyMember:
                    typer.secho(f"❌ {student.name} is already a member.", fg=typer.colors.RED)
            else:
                typer.secho("❌ Student not found.", fg=typer.colors.RED)

        elif choice == "Remove Member" and isinstance(member, ClubAdmin):
            member_names = [m.student.name for m in club.get_members() if m != member]  # cannot remove self
            selected_name = select_option(member_names + ["Back"], "Select a member to remove:")
            if selected_name == "Back" or selected_name is None:
                continue

            to_remove = next(m.student for m in club.get_members() if m.student.name == selected_name)
            from errors import NotMember
            try:
                member.remove_member(to_remove)
                typer.secho(f"✅ {selected_name} removed from the club.", fg=typer.colors.GREEN)
            except NotMember:
                typer.secho(f"❌ {selected_name} is not a member.", fg=typer.colors.RED)

        elif choice == "Promote Member" and isinstance(member, ClubAdmin):
            from errors import NotMember, BadFormatException
            from club_member import ClubManager, ClubMember

            eligible_members = [
                m for m in club.get_members()
                if isinstance(m, ClubMember) and not isinstance(m, (ClubManager, ClubAdmin))
            ]

            if not eligible_members:
                typer.secho("📌 No members available for promotion.", fg=typer.colors.MAGENTA)
                continue

            member_names = [m.student.name for m in eligible_members]
            selected_name = select_option(member_names + ["Back"], "Select a member to promote:")

            if selected_name == "Back" or selected_name is None:
                continue

            to_promote = next(m for m in eligible_members if m.student.name == selected_name)

            try:
                member.promote_member(to_promote)
                typer.secho(f"✅ {selected_name} has been promoted to Manager!", fg=typer.colors.GREEN)
            except BadFormatException as e:
                typer.secho(f"❌ {e}", fg=typer.colors.RED)
            except NotMember as e:
                typer.secho(f"❌ {e}", fg=typer.colors.RED)

        elif choice == "Back" or choice is None:
            break


if __name__ == "__main__":
    app()
