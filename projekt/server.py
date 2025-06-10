import socket
import select

import lib.SockArr as sa

def getDiscoverySocket(port) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('', port))
    sock.setblocking(False)
    return sock

def getListeningSocket(port) -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #zeby sie nie blokowalo, bo sa bugi czasem
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    sock.bind(('', port))
    sock.listen()

    return sock

if __name__ == '__main__':
    port = 3490
    max_msg_size = 1024

    discoverySocket = getDiscoverySocket(port)
    serverSocket = getListeningSocket(port)
    sockets = sa.SockArr()

    sockets.addSocket(discoverySocket)
    sockets.addSocket(serverSocket)

    while True:

        events = sockets.poller.poll(1000) #1 sekunda

        print('poll')
        if not events: continue

        for fd, event in events:
            if not (event & select.POLLIN): continue

            if fd == discoverySocket.fileno():
                #mamy probe odkrycia
                msg, sender = discoverySocket.recvfrom(max_msg_size)
                discoverySocket.sendto(b'b', sender)

            elif fd == serverSocket.fileno():
                #mamy probe polaczenia
                new_sock,_ = serverSocket.accept() #tu zamiast _ mozna zebrac adres
                sockets.addSocket(new_sock)
                print('registered a new client')

            else:
                #jeden z klientow cos od nas chce
                sock = sockets.getSocket(fd)
                data = sock.recv(max_msg_size)

                if not data:
                    #to znaczy ze sie odlaczyl
                    sockets.rmSocket(fd)
                    print('a client disconnected')

