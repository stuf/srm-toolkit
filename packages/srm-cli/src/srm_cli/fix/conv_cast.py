from pathlib import Path
from typing import Annotated

import async_typer as typer
from rich.progress import Progress

from srm_cli.parsing import parse_bfres_stdout

app = typer.Typer()


def validate_bfrestocast_bin_path(val: Path):
    pass


@app.command()
def conv_cast(
    path: Path,
    binpath: Annotated[Path,
                       typer.Argument(envvar='SRM_BFRESTOCAST_BIN',
                                      callback=validate_bfrestocast_bin_path)],
    verbose: Annotated[bool,
                       typer.Option('-v/-q', '--verbose/--quiet')] = False,
    recurse: Annotated[bool,
                       typer.Option('-r', '--recurse/--no-recurse')] = False):
    """Utility to batch-convert bfres files into the cast format
    """

    import subprocess

    if not path.exists():
        raise FileNotFoundError('given path does not exist')

    globs = ['*.bfres', '*.bfres.zs']
    filelist: list[Path] = []
    tasks_done: dict = {}

    for glob in globs:
        files = path.rglob(glob) if recurse else path.glob(glob)
        filelist += list(files)

    with Progress() as progress:
        task = progress.add_task('Convert bfres to cast')

        for file in filelist:
            progress.update(
                task,
                description=f'Convert {file.name}',
                advance=1,
            )
            cmd = [str(binpath), str(file)]

            try:
                res = subprocess.run(
                    cmd,
                    encoding='UTF-8',
                    capture_output=True,
                    check=True,
                )
                out = parse_bfres_stdout(res.stdout)
                tasks_done[str(file)] = out
            except subprocess.CalledProcessError as e:
                print('FALERT')
                print(e)


if __name__ == '__main__':
    app()
