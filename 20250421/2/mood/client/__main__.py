import argparse
from . import client
import sys

parser = argparse.ArgumentParser()
parser.add_argument("username")
parser.add_argument("--host", default="localhost")
parser.add_argument("--port", type=int, default=1337)
parser.add_argument("--file", default=None)
args = parser.parse_args()

src = open(args.file) if args.file else sys.stdin
client(args.username, src, args.host, args.port)
if args.file:
    src.close()