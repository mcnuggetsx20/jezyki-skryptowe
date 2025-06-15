import select

class SockArr:
    def __init__(self):
        self.sock_dct = dict()
        self.poller = select.poll()
        return

    def getSocket(self, fd):
        # print(f'get{fd}')
        return self.sock_dct[fd]

    def addSocket(self, sock, events = select.POLLIN):
        print(f'add {sock.fileno()}')
        self.poller.register(sock, events)
        self.sock_dct[sock.fileno()] = sock
        return

    def rmSocket(self, fd):
        print(f'rm{fd}')
        del self.sock_dct[fd]
        self.poller.unregister(fd)
        return

    def modSocket(self, fd, events):
        self.poller.modify(fd, events)

