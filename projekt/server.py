import socket
import select
import struct
import cv2
import numpy as np

from collections import defaultdict
import lib.SockArr as sa
import lib.handlers as hndlrs
from lib.commands import *
from lib.types import *

class Server:

    def __init__(self):
        self.port = 3490
        self.MSG_FROM_SERVER = b'serverup'


        self.broadcastSocket = self.getBroadcastSocket(self.port)
        self.serverSocket = self.getListeningSocket(self.port)
        self.sockets = sa.SockArr()

        self.sockets.addSocket(self.serverSocket)

        # to jest sygnal ze se wstalismy
        self.send_queue = defaultdict(lambda: list())
        self.recv_queue = list()

        return

    def sendBroadcast(self):
        self.broadcastSocket.sendto(self.MSG_FROM_SERVER, ('255.255.255.255', self.port))
        return

    def getBroadcastSocket(self,port) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        sock.bind(('', port))

        sock.setblocking(False)
        return sock

    def getListeningSocket(self,port) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        #zeby sie nie blokowalo, bo sa bugi czasem
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        sock.bind(('', port))
        sock.listen()

        return sock

    def clean(self, fd):
        self.sockets.getSocket(fd).close()
        self.sockets.rmSocket(fd)
        del self.send_queue[fd]
        return

    def main_loop(self):
        try:
            while True:
                events = self.sockets.poller.poll(1000) #1 sekunda
                for i in self.send_queue.keys():
                    if self.send_queue[i]:


                # print('poll')
                if not events: continue

                for fd, event in events:
                    current_socket = self.sockets.getSocket(fd)

                    if current_socket == self.serverSocket:
                        if event & select.POLLIN:
                            #mamy probe polaczenia
                            new_sock,_ = self.serverSocket.accept() #tu zamiast _ mozna zebrac adres
                            self.sockets.addSocket(new_sock, events= select.POLLIN | select.POLLOUT)
                            print('registered a new client')

                    else:
                        if event & select.POLLIN:
                            #jeden z klientow cos od nas chce
                            # if sockets.getId(fd) == None:
                            #     msg = current_socket.recv(10)
                            #     if msg:
                            #         sockets.setId(fd, msg)
                            #
                            # elif sockets.getId(fd) == b'cam':
                            #     hdlrs.camera_handler(fd, sockets, camera_payload_size)
                            #
                            # else:
                            #     pass

                            data = b''
                            #najpierw odbieramy tylko typ komendy
                            while len(data) < 1:
                                packet = current_socket.recv(1)
                                if not packet: break
                                data += packet

                            if len(data) < 1:
                                self.clean(fd)
                                continue

                            print(len(data))
                            command = struct.unpack('!B', data[:1])[0]
                            print(f'command {command}')

                            if command == COMMAND_IDENTIFY:
                                if hndlrs.identify_handler(fd, self.sockets) == None:
                                    self.clean(fd)
                            
                            elif command == COMMAND_CAMERA_STREAM:
                                frame = hndlrs.camera_handler(fd, self.sockets)

                                if frame == None:
                                    self.clean(fd)

                                else:
                                    self.recv_queue.append({
                                        'fd': fd,
                                        'command': COMMAND_CAMERA_STREAM,
                                        'data': frame,
                                    })

                        elif event & select.POLLOUT:
                            if not self.send_queue[fd]: continue

                            data_to_send = self.send_queue[fd][0]

                            bytes_sent = current_socket.send(data_to_send)

                            if bytes_sent < len(data_to_send):
                                self.send_queue[fd][0] = data_to_send[bytes_sent:]
                            else:
                                self.send_queue[fd].pop(0)

                            if not self.send_queue:
                                self.sockets.modSocket(fd, select.POLLIN)




        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            self.serverSocket.close()
            self.broadcastSocket.close()

    def add_to_send(self, fd, data):
        self.send_queue[fd].append(data)

        return
    

if __name__ == '__main__':
    serv = Server()

    serv.main_loop()






