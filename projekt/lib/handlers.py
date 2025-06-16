import socket
import struct
import cv2
import numpy as np
from collections import defaultdict

def empty_handler():
    pass

def camera_handler(fd, sockets, camera_payload_size, 
                  MAX_FRAME_SIZE=10**6, max_msg_size = 4096):
    sock = sockets.getSocket(fd)
    data = b''

    while len(data) < camera_payload_size:
        print('1st loop')
        packet = sock.recv(max_msg_size)
        if not packet: break
        data += packet

    if len(data) < camera_payload_size:
        #to znaczy ze sie odlaczyl
        sockets.rmSocket(fd)
        print('a client disconnected')
        cv2.destroyAllWindows()

        return

    packed_size = data[:camera_payload_size]
    data = data[camera_payload_size:]

    size= struct.unpack('!I', packed_size)[0]
    if size > MAX_FRAME_SIZE: 
        return

    while len(data) < size:
        # print('2nd loop', len(data), size)

        packet = sock.recv(max_msg_size)
        if not packet: break
        data += packet

    if not data:
        #to znaczy ze sie odlaczyl
        sockets.rmSocket(fd)
        print('a client disconnected')

    frame_data = data[:size]
    data = data[size:]    

    nparr = np.frombuffer(frame_data, dtype=np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    cv2.imshow('Klient', frame)
    cv2.waitKey(1)

    return
