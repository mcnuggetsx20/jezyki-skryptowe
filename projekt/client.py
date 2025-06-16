import socket
import select

import lib.SockArr as sa

class Client:
    def __init__(self):
        self.clientSocket = None
        self.serverInfo = (None, None)
        self.sockets = sa.SockArr()
        self.client_connected = False

        self.send_queue = list()

        self.MSG_SIZE = 1024
        self.PORT = 3490
        self.MSG_FROM_SERVER = b'serverup'

        return;

    def getDgramSocket(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(('', port))

        sock.setblocking(False)
        return sock

    def getClientSocket(self, port) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        sock.setblocking(False)

        # tutaj bindujemy pomimo tego ze jest pozniej
        # connect() bo chcemy ten port czym predzej zarezerwowac
        sock.bind(('', port))

        return sock

    def pollEvents(self, timeout = 1000):
        events = self.sockets.poller.poll(timeout)
        # if not events: return

        for fd, event in events:
            current_socket = self.sockets.getSocket(fd)

            if current_socket == self.clientSocket:

                if not self.client_connected and (event & select.POLLOUT):
                    err = current_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                    if err:
                        current_socket.close()
                        self.sockets.rmSocket(fd)
                        self.client_connected = False
                    else:
                        #zmiana eventa z POLLOUT na POLLIN
                        print('established a tcp connection')
                        self.sockets.modSocket(fd, select.POLLIN | select.POLLOUT)
                        self.client_connected = True
                    continue

                if self.client_connected:
                    if event & select.POLLIN:
                        msg, _ = current_socket.recv(self.MSG_SIZE)
                        if msg:
                            pass
                        else:
                            # tutaj nam sie tcp rozlaczyl
                            self.client_connected = False
                            current_socket.close()
                            self.sockets.rmSocket(fd)

                    elif (event & select.POLLOUT) and self.send_queue:
                        data_to_send = self.send_queue[0]
                        print(len(data_to_send))
                        bytes_sent = current_socket.send(data_to_send)

                        if bytes_sent < len(data_to_send):
                            # self.send_queue[0] = data_to_send[bytes_sent:]
                            pass
                        else:
                            self.send_queue.pop(0)

                        if not self.send_queue:
                            self.sockets.modSocket(fd, select.POLLIN)

            else:

                # tutaj nasz socket udp cos zwrocil,
                # my go uzywamy tylko do laczenia sie z serwerem
                # wiec jesli nie potrzebujemy polaczenia 
                # (bo np je juz mamy) to elo
                print(f'else {fd}')


                if self.clientSocket: return

                msg, sender = current_socket.recvfrom(self.MSG_SIZE)

                if msg == self.MSG_FROM_SERVER:
                    self.clientSocket = self.getClientSocket(self.PORT)

                    # tutaj tak trzeba bo mamy non-blocking na clientSocket
                    try: self.clientSocket.connect(sender)
                    except BlockingIOError: pass

                    self.sockets.addSocket(self.clientSocket, events=select.POLLOUT)

        return

    def add_to_send(self, data):
        self.send_queue.append(data)

    def prepare(self):
        # self.clientSocket = self.getClientSocket(self.PORT)

        # self.sockets.addSocket(self.clientSocket)
        self.sockets.addSocket(self.getDgramSocket(self.PORT))

if __name__ == '__main__':
    client = Client()
    client.prepare()
    while True:
        client.pollEvents()

