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
    try:
        typer.echo("\n" + "="*30)
        typer.secho("📝 Student Registration", fg=typer.colors.BLUE, bold=True)
        typer.echo("="*30)

        student = Student()

        result = student.register()

        if result:
            typer.secho("✅ Registration successful!", fg=typer.colors.GREEN, bold=True)
        else:
            typer.secho("❌ Registration failed!", fg=typer.colors.RED, bold=True)

    except Exception as e:
        typer.secho(f"❌ Error during registration: {str(e)}", fg=typer.colors.RED)
        typer.secho("Please try again or contact support.", fg=typer.colors.YELLOW)

def handle_login():
    try:
        typer.echo("\n" + "="*30)
        typer.secho("📝 Student Registration", fg=typer.colors.BLUE, bold=True)
        typer.echo("="*30)

        student = Student()

        result = student.login()

        if result:
            typer.secho("✅ Login successful!", fg=typer.colors.GREEN, bold=True)
        else:
            typer.secho("❌ Login failed!", fg=typer.colors.RED, bold=True)
            typer.secho("Please check your credentials and try again.", fg=typer.colors.YELLOW)

    except:
        typer.secho(f"❌ Error during login: {str(e)}", fg=typer.colors.RED)
        typer.secho("Please try again or contact support.", fg=typer.colors.YELLOW)


if __name__ == "__main__":
    app()
