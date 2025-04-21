import io
import unittest
from mood import client
from unittest.mock import MagicMock, patch


class TestClient(unittest.TestCase):
    def setUp(self):
        self.sockfd = MagicMock()
        self.sockfd.sendall = lambda s: setattr(self.sockfd, "data", s)
        self.sockfd.recv = lambda size: self.sockfd.data[:size]

    def test_0_cl(self):
        with patch("sys.stdin", io.StringIO("up\n")) as stdin:
            client.MUD(self.sockfd, stdin).cmdloop()
            self.assertEqual(self.sockfd.data.decode().rstrip(), "move 0 -1")

    def test_1_cl(self):
        with patch("sys.stdin", io.StringIO("right\n")) as stdin:
            client.MUD(self.sockfd, stdin).cmdloop()
            self.assertEqual(self.sockfd.data.decode().rstrip(), "move 1 0")

    def test_2_cl(self):
        with patch("sys.stdin", io.StringIO("addmon daemon hello hello coords 1 0 hp 50\n")) as stdin:
            client.MUD(self.sockfd, stdin).cmdloop()
            self.assertEqual(self.sockfd.data.decode().rstrip(), "addmon daemon 50 1 0 hello")

    def test_3_cl(self):
        with patch("sys.stdin", io.StringIO("attack daemon\n")) as stdin:
            client.MUD(self.sockfd, stdin).cmdloop()
            self.assertEqual(self.sockfd.data.decode().rstrip(), "attack daemon 10")

    def test_4_cl(self):
        with patch("sys.stdin", io.StringIO("down town\n")) as stdin:
            client.MUD(self.sockfd, stdin).cmdloop()
            self.sockfd.return_value.sendall.assert_not_called()

    def test_5_cl(self):
        with patch("sys.stdin", io.StringIO("attack daemon with ak47\n")) as stdin:
            client.MUD(self.sockfd, stdin).cmdloop()
            self.sockfd.return_value.sendall.assert_not_called()
