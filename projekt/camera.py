import cv2
import pickle
import client
import struct

def getCam(device : int | str = 0) -> tuple[cv2.VideoCapture, int, int]:
    camera = cv2.VideoCapture(device)

    if not camera.isOpened():
        print('couldnt open video capture device')
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

if __name__ == '__main__':
    camera, width, height = getCam()
    cl = client.Client()
    cl.prepare()

    while True:
        ret, frame = camera.read()
        if not ret:
            raise Exception("Failed to read frame!")

        if cl.client_connected:
            _, encoded = cv2.imencode('.jpg', frame)
            data = pickle.dumps(encoded)
            cl.add_to_send(struct.pack('!I', len(data)) + data)


        cl.pollEvents(timeout=0)

    camera.release()
    cv2.destroyAllWindows()
