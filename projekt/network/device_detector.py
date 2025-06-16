import socket

class DeviceDetector():
    def __init__(self, port=3490, msg_from_server = 'serverup'):
        self.port = port
        self.msg_from_server = msg_from_server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
        self.sock.bind(('', port))
        self.sock.setblocking(False)
        
    def broadcast_send_msg(self):
        self.sock.sendto(self.msg_from_server, ('255.255.255.255', self.port))