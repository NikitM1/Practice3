import multiprocessing
import socket
import time
import unittest
from mood import server


class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.addr = ("localhost", 7357)
        cls.proc = multiprocessing.Process(target=server.server, args=cls.addr)
        cls.proc.start()
        time.sleep(1)
        cls.sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cls.sockfd.connect(cls.addr)
        cls.sockfd.sendall(b"tester\n")
        cls.sockfd.recv(1)
        cls.sockfd.sendall(b"movemonsters off\n")
        cls.sockfd.recv(128)

    def test_0_srv(self):
        self.sockfd.sendall(b"addmon daemon 50 1 0 hi\n")
        _data = self.sockfd.recv(128).decode().rstrip()
        self.assertEqual(
            _data,
            "Added monster daemon to (1, 0) saying hi"
        )

    def test_1_srv(self):
        self.sockfd.sendall(b"move 1 0\n")
        _data = self.sockfd.recv(1024).decode().rstrip()
        self.assertEqual(_data, r"""Moved to (1, 0)
 ____ 
< hi >
 ---- 
   \         ,        ,
    \       /(        )`
     \      \ \___   / |
            /- _  `-/  '
           (/\/ \ \   /\
           / /   | `    \
           O O   ) /    |
           `-^--'`<     '
          (_.)  _  )   /
           `.___/`    /
             `-----' /
<----.     __ / __   \
<----|====O)))==) \) /====
<----'    `--' `.__,' \
             |        |
              \       /
        ______( (_  / \______
      ,'  ,-----'   |        \
      `--{__________)        \/""")

    def test_2_srv(self):
        self.sockfd.sendall(b"attack daemon 10\n")
        time.sleep(0.125)
        _data = self.sockfd.recv(128).decode().rstrip()
        self.assertEqual(
            _data, """Attacked daemon, damage 10 hp
daemon now has 40""")

    def test_3_srv(self):
        self.sockfd.sendall(b"attack daemon 15\n")
        time.sleep(0.125)
        _data = self.sockfd.recv(128).decode().rstrip()
        self.assertEqual(
            _data, """Attacked daemon, damage 15 hp
daemon now has 25""")

    def test_4_srv(self):
        self.sockfd.sendall(b"attack daemon 20\n")
        time.sleep(0.125)
        _data = self.sockfd.recv(128).decode().rstrip()
        self.assertEqual(
            _data, """Attacked daemon, damage 20 hp
daemon now has 5""")

    def test_5_srv(self):
        self.sockfd.sendall(b"attack daemon 10\n")
        time.sleep(0.125)
        _data = self.sockfd.recv(128).decode().rstrip()
        self.assertEqual(
            _data, """Attacked daemon, damage 5 hp
daemon died""")

    def test_6_srv(self):
        self.sockfd.sendall(b"attack daemon 10\n")
        time.sleep(0.125)
        _data = self.sockfd.recv(128).decode().rstrip()
        self.assertEqual(_data, "No daemon here")

    @classmethod
    def tearDownClass(cls):
        cls.sockfd.close()
        cls.proc.terminate()
