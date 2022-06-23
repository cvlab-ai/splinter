import argparse
import os

parser = argparse.ArgumentParser(prog=__package__, description="Unpack answers")
parser.add_argument(
    "--search-dir",
    type=str,
    default=os.getcwd(),
    help="Directory to search for answer archives",
)
parser.add_argument(
    "--dest-dir",
    type=str,
    default=os.getcwd(),
    help="Directory to unpack answer archives into",
)
parser.add_argument(
    "--archive-re",
    type=str,
    default="answers.*\.zip",
    help="Regular expression to match answer archive name",
)

def get_args():
    return parser.parse_args()
