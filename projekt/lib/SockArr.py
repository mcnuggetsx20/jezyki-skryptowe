import select
# from collections import defaultdict


class SockArr:
    def __init__(self):
        self.sock_dct = dict()
        self.poller = select.poll()

        # self.props = defaultdict(lambda: {'type': None, 'name' : None})
        self.props = dict()
        self.default_value = {'type': None, 'name' : None, 'ip': None}

        return

    def getSocket(self, fd):
        # print(f'get{fd}')
        return self.sock_dct[fd]

    def addSocket(self, sock, address = None ,events = select.POLLIN):
        print(f'add {sock.fileno()}')
        self.poller.register(sock, events)
        self.sock_dct[sock.fileno()] = sock
        if sock.fileno() not in self.props.keys():
            self.props[sock.fileno()] = self.default_value
        if address:
            self.props[sock.fileno()]['ip'] = address[0]
        return

    def rmSocket(self, fd):
        print(f'rm{fd}')
        del self.sock_dct[fd]
        self.poller.unregister(fd)

        return

    def modSocket(self, fd, events):
        self.poller.modify(fd, events)
        return

    def setType(self, fd, id):
        if fd not in self.props.keys():
            self.props[fd] = self.default_value

        self.props[fd]['type'] = id
        return

    def getType(self, fd):
        return self.props[fd]['type'] if fd in self.props.keys() else None
    
    def getIP(self, fd):
        return self.props[fd]['ip'] if fd in self.props.keys() else None

    def setName(self, fd, name):
        if fd not in self.props.keys():
            self.props[fd] = self.default_value

        self.props[fd]['name'] = name
        return

    def getName(self, fd):
        return self.props[fd]['name'] if fd in self.props.keys() else None
        
