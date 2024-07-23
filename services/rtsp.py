import cv2

def getRtspStream(url):
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        raise RuntimeError("Could not start video capture")

    while True:
        flag, frame = cap.read()
        if not flag:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--PNPframe\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
