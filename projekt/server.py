import socket
import select
import struct
import cv2
import numpy as np

import collections
import lib.SockArr as sa
import lib.handlers as hdlrs
from lib.commands import *
from lib.types import *

def getBroadcastSocket(port) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
    sock.bind(('', port))

    sock.setblocking(False)
    return sock

def getListeningSocket(port) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #zeby sie nie blokowalo, bo sa bugi czasem
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    sock.bind(('', port))
    sock.listen()

    return sock

def main_loop():
    while True:
        events = sockets.poller.poll(1000) #1 sekunda

        print('poll')
        if not events: continue

        for fd, event in events:
            if not (event & select.POLLIN): continue
            current_socket = sockets.getSocket(fd)

            if current_socket == serverSocket:
                #mamy probe polaczenia
                new_sock,_ = serverSocket.accept() #tu zamiast _ mozna zebrac adres
                sockets.addSocket(new_sock)
                print('registered a new client')

            else:
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
                    current_socket.close()
                    sockets.rmSocket(fd)
                    continue

                print(len(data))
                command = struct.unpack('!B', data[:1])[0]
                print(f'command {command}')

                if command == COMMAND_IDENTIFY:
                    while len(data) < 3:
                        packet = current_socket.recv(max_msg_size)
                        if not packet: break
                        data += packet

                    if len(data) < 3:
                        current_socket.close()
                        sockets.rmSocket(fd)

                    device_type,name_len = struct.unpack('!BB', data[1:3])
                    device_name_packed = data[3:]

                    while len(device_name_packed) < name_len:
                        packet = current_socket.recv(max_msg_size)
                        if not packet: break
                        device_name_packed += packet

                    if len(device_name_packed) < name_len:
                        current_socket.close()
                        sockets.rmSocket(fd)

                    device_name = device_name_packed.decode('utf-8')

                    print(command, device_type, name_len, device_name)
                
                elif command == COMMAND_CAMERA_STREAM:
                    hdlrs.camera_handler(fd, sockets, camera_payload_size)

if __name__ == '__main__':
    port = 3490
    max_msg_size = 4096
    MSG_FROM_SERVER = b'serverup'
    MAX_FRAME_SIZE = 10**6

    frame_times = collections.deque(maxlen=30) 

    broadcastSocket = getBroadcastSocket(port)
    serverSocket = getListeningSocket(port)
    sockets = sa.SockArr()

    sockets.addSocket(serverSocket)

    # to jest sygnal ze se wstalismy
    broadcastSocket.sendto(MSG_FROM_SERVER, ('255.255.255.255', port))

    camera_payload_size = struct.calcsize('!I')

    try:
        main_loop()
    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        serverSocket.close()
        broadcastSocket.close()
