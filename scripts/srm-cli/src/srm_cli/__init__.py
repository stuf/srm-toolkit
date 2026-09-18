from pprint import pprint
from argparse import ArgumentParser

import srm_cli.cmds as cmds


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    sub = parser.add_subparsers(title='Subcommands')

    cmds.normals.configure(sub.add_parser('normals'))

    args = parser.parse_args()

    if 'func' in args:
        args.func(args)
