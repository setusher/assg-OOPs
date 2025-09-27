import typer
import inquirer

def select_option(options, message):
    questions = [inquirer.List('choice', message=message, choices=options)]
    answers = inquirer.prompt(questions)
    return answers['choice'] if answers else None

app = typer.Typer()

@app.command()
def menu():
    options = ["Option 1", "Option 2", "Option 3", "Exit"]
    choice = select_option(options, "Select an option")
    typer.echo(f"You chose: {choice}")

if __name__ == "__main__":
    app()