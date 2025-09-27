from student import Student
from club import Club
from assignment import Assignment
from submission import Submission
from errors import BadFormatException, InvalidPassword, AlreadyMember
import datetime
import typer
import sys
import inquirer
from typing import Optional 

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


app = typer.Typer()

@app.command()
def main_menu():
    options = ["Register", "Login", "Exit"]

    while True:
        typer.echo("\n" + "="*50)
        typer.secho("🎓 Student Management System", fg=typer.colors.CYAN, bold=True)
        typer.echo("="*50)

        choice = select_option(options, "What would you like to do?")

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
    try:
        typer.echo("\n" + "="*30)
        typer.secho("📝 Student Registration", fg=typer.colors.BLUE, bold=True)
        typer.echo("="*30)

        typer.secho("\nPlease provide the following information:", fg=typer.colors.CYAN, bold=True)

        while True:
            name = typer.prompt(" Enter your full name").strip()
            if len(name) >= 1:
                break
            typer.secho("Name cannot be empty!", fg=typer.colors.RED)

        while True:
            enrollment = typer.prompt(" Enter enrollment number (8 digits)").strip()
            if len(enrollment) == 8 and enrollment.isdigit():
                break
            typer.secho("❌ Enrollment must be exactly 8 digits!", fg=typer.colors.RED)
        
        
        while True:
            password = typer.prompt("🔒 Enter password (minimum 8 characters)", hide_input=True)
            if len(password) >= 8:
                break
            typer.secho("❌ Password must be at least 8 characters long!", fg=typer.colors.RED)
        
        
        while True:
            confirm_password = typer.prompt("🔒 Confirm password", hide_input=True)
            if password == confirm_password:
                break
            typer.secho("❌ Passwords do not match!", fg=typer.colors.RED)

        student = Student()
        student.name = name
        student.enrollment = enrollment
        student.password = password

        typer.echo("\n" + "="*40)
        typer.secho("📋 Registration Details:", fg=typer.colors.BLUE, bold=True)
        typer.echo(f"Name: {name}")
        typer.echo(f"Enrollment: {enrollment}")
        typer.echo(f"Email: {email if email else 'Not provided'}")
        typer.echo(f"Phone: {phone if phone else 'Not provided'}")
        typer.echo("="*40)
        
        if typer.confirm("\n✅ Proceed with registration?"):
            result = student.register()
            
            if result:
                typer.secho("\n🎉 Registration successful!", fg=typer.colors.GREEN, bold=True)
                typer.secho(f"Welcome {name}! You can now login with enrollment: {enrollment}", 
                           fg=typer.colors.CYAN)
            else:
                typer.secho("\n❌ Registration failed!", fg=typer.colors.RED, bold=True)
        else:
            typer.secho("\n❌ Registration cancelled.", fg=typer.colors.YELLOW)

    except:
        pass


def handle_login():
    try:
        typer.echo("\n" + "="*30)
        typer.secho("📝 Student Login", fg=typer.colors.BLUE, bold=True)
        typer.echo("="*30)

        typer.secho("\nPlease enter your credentials:", fg=typer.colors.CYAN, bold=True)

        while True:
            enrollment = typer.prompt("Enrollment number").strip()
            if len(enrollment) == 8 and enrollment.isdigit():
                break
            typer.secho("❌ Please enter a valid 8-digit enrollment number!", fg=typer.colors.RED)

            password = typer.prompt("🔒 Password", hide_input=True)

            student = Student()


            if result:
                typer.secho(f"\n🎉 Welcome back!", fg=typer.colors.GREEN, bold=True)
                typer.secho(f"Successfully logged in with enrollment: {enrollment}", fg=typer.colors.CYAN)

            else:
                typer.secho("\n❌ Login failed!", fg=typer.colors.RED, bold=True)
                typer.secho("Please check your enrollment number and password.", fg=typer.colors.YELLOW)

    except:
        pass        




    

if __name__ == "__main__":
    app()
