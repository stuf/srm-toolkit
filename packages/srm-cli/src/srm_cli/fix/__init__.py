import async_typer as typer

from srm_cli.fix.fix_normalmaps import app as fix_normalmaps
from srm_cli.fix.fix_alpha import app as fix_alpha
from srm_cli.fix.conv_cast import app as conv_cast

app = typer.Typer()
app.add_typer(fix_normalmaps)
app.add_typer(fix_alpha)
app.add_typer(conv_cast)
