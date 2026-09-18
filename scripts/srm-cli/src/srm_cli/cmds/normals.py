from argparse import ArgumentParser
from pprint import pprint
from PIL import Image
from PIL.ImageOps import invert
from pathlib import Path


def configure(parser: ArgumentParser):
    parser.set_defaults(func=run)
    parser.add_argument('path', help='input dir', type=Path)
    parser.add_argument('--suffix', default='Nrm')
    parser.add_argument('-r',
                        '--recursive',
                        help='Recursive',
                        action='store_true')


def run(args) -> None:
    files = Path(args.path).rglob('*.png')
    filelist = [f for f in files if f.stem.endswith(args.suffix)]

    for file in filelist:
        im = Image.open(file)

        if im.mode == 'RGBA':
            r, g, b, a = im.split()
            rr, gr, br, ar = im.getextrema()

            bmin, bmax = br

            if bmin == 0:
                b = invert(b)

                im_ = Image.merge('RGBA', (r, g, b, a))

                print(f' - saving fixed normalmaps {file}')
                im_.save(file)
            else:
                print(f' - {file} did not need fixing')
