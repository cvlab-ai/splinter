import argparse
from .unpack.unpack_args import parser as unpack_parser
from .unpack.__main__ import main as unpack_main

parser = argparse.ArgumentParser(prog=__package__, description="Parse answers", parents=[unpack_parser], add_help=False)

subparsers = parser.add_subparsers(help="Unpack answers archives", dest="command")
unpack_parser = subparsers.add_parser("unpack", parents=[unpack_parser], add_help=False)
unpack_parser.set_defaults(func=unpack_main)


def get_args():
    return parser.parse_args()
