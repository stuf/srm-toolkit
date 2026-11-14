import async_typer as typer

from srm_cli.fix import app as fix

app = typer.Typer()
app.add_typer(fix)


def main():
    app()
