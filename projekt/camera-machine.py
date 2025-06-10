import cv2
import socket
import select

def getCam(device : int | str = 0) -> tuple[cv2.VideoCapture, int, int]:
    camera = cv2.VideoCapture(device)

    if not camera.isOpened():
        print('couldnt open a video capture device')
        return None, 0, 0

    ## ustawiamy najwyzsza mozliwa rozdzielczosc
    high_value = 10**5
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, high_value)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, high_value)

    width,height = map( 
        int, (
            camera.get(cv2.CAP_PROP_FRAME_WIDTH), 
            camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )
    )

    return camera, width, height

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
    camera, width, height = getCam()
    port = 3490

    discoverySocket = getDiscoverySocket(port)
    serverSocket = getListeningSocket(port)
    poller = select.poll()

    poller.register(discoverySocket, select.POLLIN)

    while True:
        # ret, frame = camera.read()
        # if not ret:
        #     raise Exception("Failed to read frame!")
        #
        # cv2.imshow('Sneak', frame)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

        events = poller.poll(1000) #1 sekunda

        if not events: continue

        for fd, event in events:
            if not (event & select.POLLIN): continue

            if fd == discoverySocket.fileno():
                #mamy probe odkrycia
                msg, sender = discoverySocket.recvfrom(1024)
                discoverySocket.sendto(b'b', sender)

            elif fd == serverSocket.fileno():
                #mamy probe polaczenia
                new_sock,_ = serverSocket.accept() #tu zamiast _ mozna zebrac adres
                poller.register(new_sock, select.POLLIN)

            else:
                #jeden z klientow cos od nas chce
                pass



    camera.release()
    cv2.destroyAllWindows()


