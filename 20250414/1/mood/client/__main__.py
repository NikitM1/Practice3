import cmd
import cowsay
import readline
import shlex
import socket
import sys
import time
import threading

# flake8: noqa W293
NAMES_LIST = cowsay.list_cows() + ['jgsbat']
SIZE = 10
WEAPON = ['sword', 'spear', 'axe']


class MUD(cmd.Cmd):
    intro = '<<< Welcome to Python-MUD 0.1 >>>'
    prompt = ''

    def __init__(self, socket, stdin=sys.stdin):
        super().__init__()
        self.socket = socket
        self.stdin = stdin
        if stdin is not sys.stdin:
            self.timeout = 1
            self.use_rawinput = False
        else:
            self.timeout = 0

    def precmd(self, data):
        time.sleep(self.timeout)
        return super().precmd(data)

    def do_up(self, args):
        """
        Move the player up one position.
        
        usage: up
        """
        if args:
            print('Invalid arguments')
        else:
            self.socket.sendall(b'move 0 -1\n')

    def do_down(self, args):
        """
        Move the player down one position.
        
        usage: down
        """
        if args:
            print('Invalid arguments')
        else:
            self.socket.sendall(b'move 0 1\n')

    def do_left(self, args):
        """
        Move the player one position to the left.
        
        usage: left
        """
        if args:
            print('Invalid arguments')
        else:
            self.socket.sendall(b'move -1 0\n')

    def do_right(self, args):
        """
        Move the player one position to the right.
        
        usage: right
        """
        if args:
            print('Invalid arguments')
        else:
            self.socket.sendall(b'move 1 0\n')

    def do_addmon(self, args):
        """
        Add a <cow-name> monster to the given position \
<coordinates>, which has <hitpoints> hitpoints and says the phrase <hello>.

        usage: addmon <cow-name> hello <cow-text> hp <hitpoints> coords \
<coordinates>
        """
        c = shlex.split(args)
        try:
            if len(c) != 8 or any(p not in c for p in
                                  ('hello', 'hp', 'coords')):
                raise ValueError
            name = c[0]
            if name not in NAMES_LIST:
                print('Cannot add unknown monster')
                return
            speech = c[c.index('hello') + 1]
            c.pop(c.index('hello') + 1)
            hitpoints = int(c[c.index('hp') + 1])
            if hitpoints <= 0:
                raise ValueError
            coords = c.index('coords')
            x, y = int(c[coords + 1]), int(c[coords + 2])
            if not (0 <= x < SIZE and 0 <= y < SIZE):
                raise ValueError
            self.socket.sendall((shlex.join(
                ['addmon', name, str(hitpoints), str(x), str(y), speech]
            ) + '\n').encode())
        except ValueError:
            print('Invalid arguments')

    def do_attack(self, args):
        """
        Attack a <cow-name> monster at the player's position using <weapon> \
(default: sword).

        usage: attack <cow-name> [with <weapon>]
        """
        c = shlex.split(args)
        if len(c) not in (1, 3) or 'with' in c and c.index('with') != 1:
            print('Invalid arguments')
            return
        if len(c) == 3:
            if (weapon := c[2]) not in WEAPON:
                print('Unknown weapon')
                return
        else:
            weapon = 'sword'
        self.socket.sendall((shlex.join(
            ['attack', c[0], str(10 + WEAPON.index(weapon) * 5)]
        ) + '\n').encode())

    def complete_attack(self, text, line, begidx, endidx):
        args = shlex.split(line[:begidx], False, False)
        if args[-1] == 'attack':
            return [c for c in NAMES_LIST if c.startswith(text)]
        elif args[-1] == 'with':
            return [c for c in WEAPON if c.startswith(text)]

    def do_sayall(self, args):
        """
        Send your message to all active players.
        
        usage: sayall <text>
        """
        c = shlex.split(args)
        if len(c) != 1:
            print('Invalid arguments')
            return
        self.socket.sendall((shlex.join(['sayall', c[0]]) + '\n').encode())

    def do_movemonsters(self, args):
        """
        Switch a monsters movements mode.
        
        usage: movemonsters <mode>
        """
        c = shlex.split(args)
        if len(c) != 1 or c[0] not in ('on', 'off'):
            print('Invalid arguments')
            return
        self.socket.sendall((shlex.join(['movemonsters', c[0]]) + '\n').encode())

    def do_EOF(self, args):
        self.socket = None
        return 1

    def do_default(self):
        print('Invalid command')


def listen(cmdline):
    while cmdline.socket is not None:
        data = b''
        while len(new := cmdline.socket.recv(1024)) == 1024:
            data += new
        data += new
        print(f"\n{data.decode().rstrip()}",
              f"\n{cmdline.prompt}{readline.get_line_buffer()}",
              sep='', end='', flush=True)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Username was not provided')
        exit(1)

    host = "localhost" if len(sys.argv) < 3 or not sys.argv[2].isnumeric() else sys.argv[2]
    port = 1337 if len(sys.argv) < 4 or not sys.argv[3].isnumeric() else int(sys.argv[3])

    if 'libedit' in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sockfd:
        try:
            sockfd.connect((host, port))
        except Exception:
            print('Connection refused')
            exit()
        sockfd.sendall(f"{sys.argv[1]}\n".encode())
        if int(sockfd.recv(1).decode()):
            print(f"Connected to {host}:{port}")

            src = sys.stdin if '--file' not in sys.argv else open(sys.argv[sys.argv.index('--file') + 1])
            cmdline = MUD(sockfd, src)
            listener = threading.Thread(target=listen, args=(cmdline,))
            listener.daemon = True
            listener.start()
            cmdline.cmdloop()
            src.close()
        else:
            print('Connection refused')