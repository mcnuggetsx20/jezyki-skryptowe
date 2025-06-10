import socket

def findServer(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True,)

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

if __name__ == '__main__':
    camera_addr, camera_port = findServer(3490)
