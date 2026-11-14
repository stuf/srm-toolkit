from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Annotated

from devtools import debug
from rich.pretty import pprint
from PIL import Image
from PIL.ImageOps import invert
import async_typer as typer
from rich.progress import Progress, track

from srm_cli.util import pluralize
from srm_cli.output import con

app = typer.Typer()


@dataclass(init=False)
class Stats:
    already_handled: int = 0
    handled: int = 0
    filecount: int = 0


@app.command()
def fix_normalmaps(
    path: Path,
    suffix: Annotated[str, typer.Option('--suffix')] = 'Nrm',
    dry_run: Annotated[
        bool,
        typer.Option('--dry-run', '-n', help='Don\'t make any changes'
                     )] = False,
    verbose: Annotated[bool,
                       typer.Option('--verbose/--quiet', '-v/-q')] = False,
    recursive: Annotated[
        bool, typer.Option('--recursive/--no-recurse', '-r')] = True):
    """Naïvely add a blue color channel to red-green normalmaps.
    """

    stats = Stats()

    files = path.rglob('*.png') if recursive else path.glob('*.png')
    filelist = [f for f in files if f.stem.endswith(suffix)]

    stats.filecount = len(filelist)

    with Progress() as progress:
        task = progress.add_task('converting', total=stats.filecount)

        for file in filelist:

            progress.update(task,
                            description=f'Process {file.name: <36}',
                            advance=1)
            im = Image.open(file)

            if im.mode == 'RGBA':
                r, g, b, a = im.split()
                rr, gr, br, ar = im.getextrema()

                bmin, bmax = br

                if bmin == 0:
                    b = invert(b)

                    im_ = Image.merge('RGBA', (r, g, b, a))

                    if not dry_run:
                        im_.save(file)
                    stats.handled += 1
                else:
                    stats.already_handled += 1

        progress.update(task, description='Done processing all files')

    out = []
    out += [f"{pluralize(stats.filecount, 'file')} in total"]

    if stats.already_handled > 0:
        out += [
            f"{pluralize(stats.already_handled, 'file')} already processed",
        ]

    if stats.handled > 0:
        out += [
            f"{pluralize(stats.handled, 'file')} processed",
        ]

    for l in out:
        con.print(f' - {l}')
