# it only works on esp32

import socket
import select
import struct
import time

import lib.SockArr as sa
from lib.commands import *
from lib.types import *

class Client:
    def __init__(self, tp, identity, input_handler=None):
        self.clientSocket = None
        self.serverInfo = (None, None)
        self.sockets = sa.SockArr()
        self.client_connected = False
        self.input_handler = input_handler
        self.send_queue = list()
        self.identity = identity
        self._type = tp

        self.MSG_SIZE = 1024
        self.PORT = 3490
        self.MSG_FROM_SERVER = b'serverup'

        self.COMMAND_PORT = 3501

        return

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

                #if not self.client_connected and (event & select.POLLOUT):
                 #   err = current_socket.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
                  #  if err:
                   #     self.cleanup()
                    #else:
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
                            msg = current_socket.recv(self.MSG_SIZE)
                            data = b''
                            if msg:
                                if self.input_handler:
                                    self.input_handler.handle_data(msg)

                                # tutaj nam sie tcp rozlaczyl
                        except Exception as e:
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

            elif current_socket == self.discovery_socket:
                # odbieranie broadcastu / pakietów na 3490
                try:
                    msg, sender = current_socket.recvfrom(self.MSG_SIZE)
                    if self.client_connected:
                        continue
                    if msg == self.MSG_FROM_SERVER:
                        self.clientSocket = self.getClientSocket(self.PORT)
                        try: self.clientSocket.connect(sender)
                        except : pass
                        self.sockets.addSocket(self.clientSocket, events=select.POLLOUT)
                except:
                    pass

            elif current_socket == self.command_socket:
                # tu odbieramy komendy wysyłane przez serwer na port 3500
                try:
                    msg, sender = current_socket.recvfrom(self.MSG_SIZE)
                    print(f"Received command from server {sender}: {msg}")
                    # Tu możesz dodać obsługę komend - np. wywołać funkcję
                    self.input_handler.handle_data(msg)
                except :
                    pass

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
        self.discovery_socket = self.getDgramSocket(self.PORT)
        self.sockets.addSocket(self.discovery_socket)

        # UDP socket do odbioru poleceń
        self.command_socket = self.getDgramSocket(self.COMMAND_PORT)
        self.sockets.addSocket(self.command_socket)

if __name__ == '__main__':
    client = Client(1,"led223")
    client.prepare()
    while True:
        client.pollEvents()



