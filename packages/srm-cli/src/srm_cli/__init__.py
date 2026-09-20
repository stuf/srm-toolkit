import time
import logging
from pprint import pprint

from PIL import Image
from PIL.ImageOps import invert
from pathlib import Path
from typing import Annotated, Tuple

import typer
from rich.progress import track, Progress

from .util import setup_logger, set_loglevel, pluralize

logger = logging.getLogger(__name__)

app = typer.Typer(help='Oft-wished-for utilities and tools',
                  no_args_is_help=True)


@app.command()
def normalfix(
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
    set_loglevel(logger, verbose)

    files = path.rglob('*.png') if recursive else path.glob('*.png')
    filelist = [f for f in files if f.stem.endswith(suffix)]

    already_handled = 0
    handled_filecount = 0
    filecount = len(filelist)

    logger.info(f'{pluralize(filecount, "file")} found.')

    for file in track(filelist, description="Processing", transient=True):
        im = Image.open(file)

        if im.mode == 'RGBA':
            r, g, b, a = im.split()
            rr, gr, br, ar = im.getextrema()

            bmin, bmax = br

            if bmin == 0:
                b = invert(b)

                im_ = Image.merge('RGBA', (r, g, b, a))

                logger.debug(' - saving fixed normalmap %s', file)
                if not dry_run:
                    im_.save(file)
                handled_filecount += 1
            else:
                already_handled += 1

    logger.info(f'{pluralize(filecount, "file")} total.')
    logger.info(f'{pluralize(handled_filecount, "file")} processed')
    logger.info(f'{pluralize(already_handled, "file")} already processed')


#


@app.command()
def alpha(
        path: Path,
        suffix: Annotated[str, typer.Option('--suffix')] = 'Alb',
        verbose: Annotated[bool,
                           typer.Option('--verbose/--quiet', '-v/-q')] = False,
        recursive: Annotated[bool, typer.Option('--recursive', '-r')] = False,
        output_suffix: Annotated[str, typer.Option('--output-suffix')] = 'Opa',
        dry_run: Annotated[bool, typer.Option('--dry-run', '-n')] = False):
    """Handle (usually Spl2) Alb textures that use alpha channels,
       extract alpha channel into its own texture."""
    set_loglevel(logger, verbose)

    files = path.rglob('*.png') if recursive else path.glob('*.png')
    filelist = [f for f in files if f.stem.endswith(suffix)]
    filecount = len(filelist)
    not_handled = 0
    already_handled = 0
    handled_filecount = 0

    logger.info('Files to process: %s', filecount)

    for f in track(filelist, 'Separating alpha maps'):
        im = Image.open(f)
        filepath = Path(f)
        opa_stem = filepath.stem.replace(suffix, '') + output_suffix

        fpp = list(filepath.parts)
        fpp[-1] = f'{opa_stem}{filepath.suffix}'
        opa_filepath = Path(*fpp)

        if opa_filepath.exists():
            already_handled += 1
            continue

        alpha = im.getchannel('A')

        pix_min, pix_max = alpha.getextrema()

        # If the minimum alpha is 255 there is probably no alpha at all
        if pix_min == 255:
            not_handled += 1
            continue

        alpha_image = Image.new('RGBA', im.size, (0, 0, 0, 255))
        alpha_image.paste(alpha, mask=alpha)
        alpha_image.convert('L')

        # Finally save the image
        if not dry_run:
            alpha_image.save(str(opa_filepath))

        handled_filecount += 1

    logger.info(f'{pluralize(handled_filecount, "file")} processed.')
    logger.info(
        f'{pluralize(already_handled, "file")} already processed, skipped.')
    logger.info(
        f'{pluralize(not_handled, "file")} not processed; no alpha in file.')
    logger.info(f'{pluralize(filecount, "file")} in total')


def validate_bfrestocast_bin(val: Path):
    """Validate path to BfresToCast is valid"""
    if not val.exists():
        raise typer.BadParameter('binpath does not exist')

    if not val.is_file():
        raise typer.BadParameter('binpath is not a path to a file')


@app.command()
def cast(
    path: Path,
    binpath: Annotated[Path,
                       typer.Argument(envvar='SRM_BFRES_TO_CAST_BIN_PATH',
                                      callback=validate_bfrestocast_bin)],
    verbose: Annotated[bool,
                       typer.Option('--verbose/--quiet', '-v/-q')] = False,
    recursive: Annotated[
        bool, typer.Option('--recursive/--no-recurse', '-r')] = False,
):
    """Utility to batch-convert bfres files into the cast format
    """
    import subprocess
    from .parsing import parse_bfres_stdout

    set_loglevel(logger, verbose)
    if not path.exists():
        raise FileNotFoundError('given path does not exist')

    globs = ['*.bfres', '*.bfres.zs']
    logger.debug(f'using globs {globs}')
    filelist: list[Path] = []
    tasks_done: dict[str, list[str]] = {}

    for glob in globs:
        files = path.rglob(glob) if recursive else path.glob(glob)
        filelist.extend(list(files))

    logger.info('First run after a while may take longer than usual.')

    for f in track(filelist, 'Converting bfres to cast', transient=True):
        cmd = [str(binpath), str(f)]
        logger.debug(f'{cmd=}')

        try:
            res = subprocess.run(cmd,
                                 encoding='UTF-8',
                                 capture_output=True,
                                 check=True)

            out = parse_bfres_stdout(res.stdout)
            tasks_done[str(f)] = out
        except subprocess.CalledProcessError as e:
            logger.error('error in running cmd %s', ' '.join(cmd), extra=e)

    res = tasks_done.keys()
    logger.info('%s file(s) converted', len(res))
    logger.info(' - %s', ', '.join(res))


#


def main() -> None:
    setup_logger(logger)
    app()


if __name__ == '__main__':
    main()
