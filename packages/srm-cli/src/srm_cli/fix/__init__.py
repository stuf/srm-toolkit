from srm_cli.fix.normalmaps import app as normalmaps

import async_typer as typer

app = typer.Typer()
app.add_typer(normalmaps)
