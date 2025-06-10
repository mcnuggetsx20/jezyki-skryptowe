import select

class SockArr:
    def __init__(self):
        self.sock_dct = dict()
        self.poller = select.poll()
        return

    def getSocket(self, fd):
        return self.sock_dct[fd]

    def addSocket(self, sock, events = select.POLLIN):
        self.poller.register(sock, events)
        self.sock_dct[sock.fileno()] = sock
        return

    def rmSocket(self, fd):
        del self.sock_dct[fd]
        return

