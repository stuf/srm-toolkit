import time
from PIL import Image
from PIL.ImageOps import invert
from pathlib import Path
from typing import Annotated
import typer
from rich.progress import track

app = typer.Typer(help='Helpppp', no_args_is_help=True)


@app.command(name='normals')
def normals(
        path: Path,
        suffix: Annotated[str, typer.Option('--suffix')] = 'Nrm',
        dry_run: Annotated[
            bool,
            typer.Option('--dry-run', help='Don\'t make any changes')] = False,
        recursive: Annotated[bool, typer.Option('--recursive')] = True):
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
          output_suffix: Annotated[str,
                                   typer.Option('--output-suffix')] = 'Opa',
          dry_run: Annotated[bool, typer.Option('--dry-run')] = False):
    files = path.rglob('*.png')
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


#


def main() -> None:
    app()


if __name__ == '__main__':
    main()
