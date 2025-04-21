"""
MOOD server module.

Start the server.
"""

from . import server
import sys

if __name__ == '__main__':
    host = "localhost" if len(sys.argv) < 2 else sys.argv[1]
    port = 1337 if len(sys.argv) < 3 else int(sys.argv[2])
    server(host, port)
