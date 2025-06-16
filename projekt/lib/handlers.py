import socket
import struct
import cv2
import numpy as np
from collections import defaultdict

def empty_handler():
    pass

def identify_handler(fd, sockets):
    data =b''
    current_socket = sockets.getSocket(fd)
    while len(data) < 3:
        packet = current_socket.recv(3-len(data))
        if not packet: break
        data += packet

    if len(data) < 3:
        current_socket.close()
        sockets.rmSocket(fd)

    device_type,name_len = struct.unpack('!BB', data[1:3])
    device_name_packed = data[3:]

    while len(device_name_packed) < name_len:
        packet = current_socket.recv(name_len - len(device_name_packed))
        if not packet: break
        device_name_packed += packet

    if len(device_name_packed) < name_len:
        current_socket.close()
        sockets.rmSocket(fd)

    device_name = device_name_packed.decode('utf-8')

    print(device_type, name_len, device_name)
    return

def camera_handler(fd, sockets, camera_payload_size, 
                  MAX_FRAME_SIZE=10**6, max_msg_size = 4096):
    sock = sockets.getSocket(fd)
    data = b''
    camera_payload_size = struct.calcsize('!I')

    while len(data) < camera_payload_size:
        print('1st loop')
        packet = sock.recv(len(data) - camera_payload_size)
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
    print(struct.unpack('!I', packed_size))
    if size > MAX_FRAME_SIZE: 
        print('exceeded max frame size')
        print(size)
        return

    while len(data) < size:
        # print('2nd loop', len(data), size)

        packet = sock.recv(size-len(data))
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
