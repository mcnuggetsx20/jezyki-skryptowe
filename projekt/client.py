import socket

def findServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)

    sock.settimeout(1)

    while True:
        sock.sendto(b"a", ('255.255.255.255', port))
        print('scanning local network...')

        try:
            msg, sender = sock.recvfrom(1024)

        except socket.timeout:
            continue

        break

    sock.close()

    return sender

def getClientSocket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    return sock

if __name__ == '__main__':
    camera_addr, camera_port = findServer(3490)

    clientSocket = getClientSocket()
    clientSocket.connect((camera_addr, camera_port))


