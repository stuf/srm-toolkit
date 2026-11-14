import async_typer as typer

from srm_cli.fix.normalmaps import app as normalmaps
from srm_cli.fix.alpha import app as alpha
from srm_cli.fix.cast import app as cast

app = typer.Typer()
app.add_typer(normalmaps)
app.add_typer(alpha)
app.add_typer(cast)
