import unittest
import socket
import select

from lib.SockArr import SockArr  # zamień na właściwą nazwę pliku bez `.py`


class TestSockArr(unittest.TestCase):
    def setUp(self):
        self.sa = SockArr()
        self.sock1, self.sock2 = socket.socketpair()  # połączona para socketów

    def tearDown(self):
        self.sock1.close()
        self.sock2.close()

    def test_add_and_get_socket(self):
        self.sa.addSocket(self.sock1)
        fd = self.sock1.fileno()
        self.assertEqual(self.sa.getSocket(fd), self.sock1)

    def test_addSocket_sets_default_props(self):
        self.sa.addSocket(self.sock1)
        fd = self.sock1.fileno()
        self.assertEqual(self.sa.getType(fd), None)
        self.assertEqual(self.sa.getName(fd), None)
        self.assertEqual(self.sa.getIP(fd), None)

    def test_addSocket_with_address_sets_ip(self):
        self.sa.addSocket(self.sock1, address=("192.168.0.1", 1234))
        fd = self.sock1.fileno()
        self.assertEqual(self.sa.getIP(fd), "192.168.0.1")

    def test_set_and_get_type(self):
        fd = self.sock1.fileno()
        self.sa.setType(fd, "LED")
        self.assertEqual(self.sa.getType(fd), "LED")

    def test_set_and_get_name(self):
        fd = self.sock1.fileno()
        self.sa.setName(fd, "Living Room")
        self.assertEqual(self.sa.getName(fd), "Living Room")

    def test_rmSocket(self):
        self.sa.addSocket(self.sock1)
        fd = self.sock1.fileno()
        self.sa.rmSocket(fd)
        self.assertNotIn(fd, self.sa.sock_dct)

    def test_modSocket(self):
        self.sa.addSocket(self.sock1)
        fd = self.sock1.fileno()
        try:
            self.sa.modSocket(fd, select.POLLOUT)
        except Exception as e:
            self.fail(f"modSocket raised an exception: {e}")


if __name__ == '__main__':
    unittest.main()
