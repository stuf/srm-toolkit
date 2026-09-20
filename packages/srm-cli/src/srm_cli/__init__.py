import time
import logging
from pprint import pprint

from PIL import Image
from PIL.ImageOps import invert
from pathlib import Path
from typing import Annotated

import typer
from rich.progress import track

from .util import setup_logger, set_loglevel

logger = logging.getLogger(__name__)

app = typer.Typer(help='Helpppp', no_args_is_help=True)


@app.command(name='normals')
def normals(
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
    print(f'{path=}')
    files = path.rglob('*.png')
    filelist = [f for f in files if f.stem.endswith(suffix)]

    already_handled = 0
    handled_filecount = 0
    filecount = len(filelist)
    print(f'{filecount} file(s) in total')

    for file in track(filelist, description="Doing thing"):
        im = Image.open(file)

        if im.mode == 'RGBA':
            r, g, b, a = im.split()
            rr, gr, br, ar = im.getextrema()

            bmin, bmax = br

            if bmin == 0:
                b = invert(b)

                im_ = Image.merge('RGBA', (r, g, b, a))

                print(f' - saving fixed normalmaps {file}')
                if not dry_run:
                    im_.save(file)
                handled_filecount += 1
            else:
                already_handled += 1

    print(
        f'Handled {handled_filecount}/{filecount} file(s), {already_handled} file(s) already handled.'
    )


#


@app.command()
def alpha(path: Path,
          suffix: Annotated[str, typer.Option('--suffix')] = 'Alb',
          recursive: Annotated[bool,
                               typer.Option('--recursive', '-r')] = False,
          output_suffix: Annotated[str,
                                   typer.Option('--output-suffix')] = 'Opa',
          dry_run: Annotated[bool, typer.Option('--dry-run', '-n')] = False):
    """Handle (usually Spl2) Alb textures that use alpha channels,
       extract alpha channel into its own texture."""
    files = path.rglob('*.png') if recursive else path.glob('*.png')
    filelist = [f for f in files if f.stem.endswith(suffix)]
    filecount = len(filelist)
    not_handled = 0
    already_handled = 0
    handled_filecount = 0

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

    print(' | '.join([
        f'{handled_filecount} done',
        f'{already_handled} existed',
        f'{not_handled} no alpha',
        f'{filecount} files total',
    ]))


@app.command()
def cast(
    path: Path,
    binpath: Annotated[Path,
                       typer.Argument(envvar='SRM_BFRES_TO_CAST_BIN_PATH')],
    verbose: Annotated[bool,
                       typer.Option('--verbose/--quiet', '-v/-q')] = False,
    recursive: Annotated[
        bool, typer.Option('--recursive/--no-recurse', '-r')] = False,
):
    """Utility to batch-convert bfres files into the cast format
    """
    set_loglevel(logger, verbose)
    if not path.exists():
        raise FileNotFoundError('cant do shit')
    if not binpath.exists():
        raise FileNotFoundError('invalid binpath')

    globs = ['*.bfres', '*.bfres.zs']
    logger.debug(f'using globs {globs}')

    import subprocess
    from .parsing import parse_bfres_stdout

    for glob in globs:
        files = path.rglob(glob) if recursive else path.glob(glob)
        filelist = list(files)

        for f in filelist:
            cmd = [str(binpath), str(f)]
            logger.debug(f'{cmd=}')

            try:
                res = subprocess.run(cmd,
                                     encoding='UTF-8',
                                     capture_output=True,
                                     check=True)

                out = parse_bfres_stdout(res.stdout)

                for elem_name, elem_parts in out.items():
                    logger.info('output model %s\t%s texture(s)', elem_name,
                                len(elem_parts))

                    for part in elem_parts:
                        logger.debug(f' - {elem_name} -> {part}')
            except subprocess.CalledProcessError as e:
                logger.error('error in running cmd %s', ' '.join(cmd), extra=e)


#


def main() -> None:
    setup_logger(logger)
    app()


if __name__ == '__main__':
    main()
