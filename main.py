from student import Student
from club import Club
from assignment import Assignment
from submission import Submission
from errors import BadFormatException, InvalidPassword, AlreadyMember
import datetime
import typer
from typer import colors
import inquirer
import sys
from typing import Optional


app = typer.Typer(help="Student Management System")

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

def select_option(options, message):
    questions = [inquirer.List('choice', message=message, choices=options)]
    answers = inquirer.prompt(questions)
    return answers['choice'] if answers else None

@app.command()
def main_menu():
    options = ["Register", "login", "Exit"]
    while True:
        typer.echo("\n" + "="*50)
        typer.secho("🎓 Student Management System", fg=typer.colors.CYAN, bold=True)
        typer.echo("="*50)

        choice = select_option(options,"What would you like to choose?")

        if choice == "Register":
            handle_register()
        elif choice == "Login":
            handle_login()
        elif choice == "Exit":
            typer.secho("\n👋 Thank you for using Student Management System!",
                       fg=typer.colors.GREEN, bold=True)
        elif choice is None:
            typer.secho("\n👋 Goodbye!", fg=typer.colors.YELLOW)
            break

def handle_register():
    typer.echo("\n" + "="*30)
    typer.secho("📝 Student Registration", fg=typer.colors.BLUE, bold=True)
    typer.echo("="*30)

    name = typer.prompt("Enter your full name").strip()
    enrollment = typer.prompt("Enter enrollment number (8 digits)").strip()
    password = typer.prompt("🔒 Enter password (min 8 chars)", hide_input=True)

    student = Student(name=name, enrollment=enrollment, password=password)

    try:
        result = student.register()
        typer.secho("\n🎉 Registration successful!", fg=typer.colors.GREEN, bold=True)
        typer.secho(f"Welcome {result.name}! You can now login.", fg=typer.colors.CYAN)
    except BadFormatException as e:
        typer.secho(f"\n❌ Registration failed: {e}", fg=typer.colors.RED, bold=True)
    except InvalidPassword as e:
        typer.secho(f"\n❌ Registration failed: {e}", fg=typer.colors.RED, bold=True)


def handle_login():
    typer.echo("\n" + "="*30)
    typer.secho("📝 Student Login", fg=typer.colors.BLUE, bold=True)
    typer.echo("="*30)

    enrollment = typer.prompt("Enrollment number").strip()
    password = typer.prompt("🔒 Password", hide_input=True)

    student = Student.login(enrollment, password)

    if student:
        typer.secho(f"\n🎉 Welcome back {student.name}!", fg=typer.colors.GREEN, bold=True)
    else:
        typer.secho("\n❌ Login failed! Invalid enrollment or password.", fg=typer.colors.RED, bold=True)

if __name__ == "__main__":
    app()
