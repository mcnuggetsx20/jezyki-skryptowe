import cv2
import client
import struct
import time
from lib.types import *
from lib.commands import *



class CameraCMDHandler:
    def __init__(self):
        self.streming = False
        self.move_detection= False
        return

    def handle_data(self, msg):
        if COMMAND_CAMERA_STREAM_OFF_ONN == msg[0]:
            self.streming = msg[1]
        
        elif COMMAND_CAMERA_MOVE_DETECTED_OFF_ONN == msg[0]:
            self.move_detection = msg[1]




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

def detect_motion(prev_frame: cv2.Mat, curr_frame: cv2.Mat, min_area=500) -> bool:
    prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_gray = cv2.GaussianBlur(prev_gray, (21, 21), 0)

    curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
    curr_gray = cv2.GaussianBlur(curr_gray, (21, 21), 0)

    delta_frame = cv2.absdiff(prev_gray, curr_gray)
    thresh = cv2.threshold(delta_frame, 25, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)

    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) >= min_area:
            return True
    return False

if __name__ == '__main__':
    counter = 0
    camera, width, height = getCam()
    camera_handler = CameraCMDHandler()
    cl = client.Client(tp=TYPE_CAMERA, identity='kamerka', input_handler=camera_handler)
    cl.prepare()

    ret, prev_frame = camera.read()
    try:
        while True:
            ret, frame = camera.read()
            if not ret:
                raise Exception("Failed to read frame!")

            if camera_handler.move_detection and detect_motion(prev_frame, frame) and counter%5 == 0:
                print('byl ruch!')
                counter = counter%5
                if cl.client_connected:
                    cl.add_to_send(struct.pack('!B', COMMAND_CAMERA_MOVE_DETECTED))

            prev_frame = frame
            if cl.client_connected and camera_handler.streming:
                _, encoded = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
                data = encoded.tobytes()
                cl.add_to_send(struct.pack('!BI', 
                    COMMAND_CAMERA_STREAM, len(data)) + data)


            cl.pollEvents(timeout=0)
            time.sleep(0.02)
    except KeyboardInterrupt:
        camera.release()
        cv2.destroyAllWindows()
        cl.cleanup()
