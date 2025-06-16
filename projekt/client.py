import socket
import select
import struct
import time

import lib.SockArr as sa
from lib.commands import *
from lib.types import *

class Client:
    def __init__(self, tp, identity):
        self.clientSocket = None
        self.serverInfo = (None, None)
        self.sockets = sa.SockArr()
        self.client_connected = False

        self.send_queue = list()
        self.identity = identity
        self._type = tp

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
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sock.setblocking(False)

        # tutaj bindujemy pomimo tego ze jest pozniej
        # connect() bo chcemy ten port czym predzej zarezerwowac
        sock.bind(('', port))

        return sock

    def pollEvents(self, timeout = 1000):

        # to jest funkcja ktora wykonuje jedna iteracje normalnej petli eventow
        # wysyla self.send_queue (jesli socket tcp jest gotowy)

        if self.client_connected and self.send_queue:
            self.sockets.modSocket(self.clientSocket.fileno(), select.POLLOUT | select.POLLIN)

        events = self.sockets.poller.poll(timeout)
        # if not events: return

        for fd, event in events:
            current_socket = self.sockets.getSocket(fd)

            if current_socket == self.clientSocket:

                if not self.client_connected and (event & select.POLLOUT):
                    err = current_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                    if err:
                        self.cleanup()
                    else:
                        print('established a tcp connection')
                        self.sockets.modSocket(fd, select.POLLIN | select.POLLOUT)
                        self.client_connected = True

                        id_bytes = self.identity.encode('utf-8')
                        msg = struct.pack('!BBB', COMMAND_IDENTIFY, self._type, len(id_bytes)) + id_bytes
                        self.send_queue.append(msg) #informacja o tym kim jestesmy

                        # current_socket.send(msg) #informacja o tym kim jestesmy
                    # continue

                if self.client_connected:
                    if event & select.POLLIN:
                        try:
                            msg, _ = current_socket.recv(self.MSG_SIZE)
                            data = b''
                            #najpierw odbieramy tylko typ komendy
                            while len(data) < 1:
                                packet = current_socket.recv(1)
                                if not packet: break
                                data += packet

                            if len(data) < 1:
                                self.cleanup()
                                continue

                            command = struct.unpack('!B', data[:1])[0]
                            #if command == COMMAND_STH

                        except BlockingIOError: pass
                        except (ConnectionResetError, ValueError):
                            self.cleanup()

                    elif (event & select.POLLOUT) and self.send_queue:

                        data_to_send = self.send_queue[0]

                        bytes_sent = current_socket.send(data_to_send)
                        print(time.time(), len(data_to_send), bytes_sent)

                        if bytes_sent < len(data_to_send):
                            # self.send_queue[0]['data'] = data_to_send[bytes_sent:]
                            self.send_queue[0] = data_to_send[bytes_sent:]
                        else:
                            self.send_queue.pop(0)

                        if not self.send_queue:
                            self.sockets.modSocket(fd, select.POLLIN)

            else:

                # tutaj nasz socket udp cos zwrocil,
                # my go uzywamy tylko do laczenia sie z serwerem
                # wiec jesli nie potrzebujemy polaczenia 
                # (bo np je juz mamy) to elo
                print(f'udp enter')


                print(f'udp recv')

                msg, sender = current_socket.recvfrom(self.MSG_SIZE)
                if self.client_connected: return

                if msg == self.MSG_FROM_SERVER:
                    self.clientSocket = self.getClientSocket(self.PORT)

                    # tutaj tak trzeba bo mamy non-blocking na clientSocket
                    try: self.clientSocket.connect(sender)
                    except BlockingIOError: pass

                    self.sockets.addSocket(self.clientSocket, events=select.POLLOUT)

        return

    def add_to_send(self, data):
        self.send_queue.append(data)

    def cleanup(self):

        #ta funkcja rozlacza socket tcp i czysci co trzeba,
        # uzywac zawsze kiedy tcp sie wywala

        self.sockets.rmSocket(self.clientSocket.fileno())
        self.clientSocket.close()
        self.client_connected = False
        self.send_queue = list()
        return

    def prepare(self):
        # self.clientSocket = self.getClientSocket(self.PORT)

        # self.sockets.addSocket(self.clientSocket)
        self.sockets.addSocket(self.getDgramSocket(self.PORT))

if __name__ == '__main__':
    client = Client()
    client.prepare()
    while True:
        client.pollEvents()

