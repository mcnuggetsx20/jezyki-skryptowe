import socket
import select

import lib.SockArr as sa

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

    sock.bind(('', port))
    sock.listen()

    return sock

# def findServer(port):
#     sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, True)
#
#     sock.settimeout(1)
#
#     while True:
#         sock.sendto(b"a", ('255.255.255.255', port))
#         print('scanning local network...')
#
#         try:
#             msg, sender = sock.recvfrom(1024)
#
#         except socket.timeout:
#             continue
#
#         break
#
#     sock.close()
#
#     return sender


if __name__ == '__main__':
    port = 3490
    max_msg_size = 1024
    MSG_FROM_SERVER = b'serverup'

    broadcastSocket = getBroadcastSocket(port)
    serverSocket = getListeningSocket(port)
    sockets = sa.SockArr()

    sockets.addSocket(serverSocket)

    # to jest sygnal ze se wstalismy
    broadcastSocket.sendto(MSG_FROM_SERVER, ('255.255.255.255', port))

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
                sock = sockets.getSocket(fd)
                data = sock.recv(max_msg_size)

                if not data:
                    #to znaczy ze sie odlaczyl
                    sockets.rmSocket(fd)
                    print('a client disconnected')

