import os
import cv2
import threading
import time
import base64
from datetime import datetime
from collections import deque
from services.location import read_with_cctv

class ClipManager:
    def __init__(self, rtsp_url, fps=30):
        self.rtsp_url = rtsp_url
        self.fps = fps
        self.buffer = deque(maxlen=fps * 10)  # 10초 분량의 프레임 저장 (이전 5초, 이후 5초)
        self.cap = cv2.VideoCapture(rtsp_url)
        self.lock = threading.Lock()
        self.recording_event = threading.Event()
        self.recording_done_event = threading.Event()
        self.thread = threading.Thread(target=self.update_buffer)
        self.thread.daemon = True
        self.thread.start()

    def update_buffer(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            with self.lock:
                self.buffer.append(frame)
            if self.recording_event.is_set():
                self.recording_done_event.set()
            time.sleep(1 / self.fps)

    def start_recording(self, message):
        occured_at = datetime.fromtimestamp(message['occurred_at'])
        filename = "%s_%s_%s" % (message["location"], message["event"], occured_at)
        self.recording_event.set()
        self.recording_done_event.wait(timeout=5)
        self.save_clip(filename)
        self.recording_event.clear()
        self.recording_done_event.clear()

    def save_clip(self, filename):
        with self.lock:
            if len(self.buffer) < self.fps * 10:
                print("Not enough frames to save a clip")
                return
            path = "./static/clip"
            filename = filename.replace("-", "_").replace(":", "_").replace(" ", "_")
            filename_ext = f"{filename}.mp4"
            save_path = os.path.join(path,filename_ext)
            fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
            out = cv2.VideoWriter(save_path, fourcc, self.fps, (self.buffer[0].shape[1], self.buffer[0].shape[0]))

            for frame in list(self.buffer):
                out.write(frame)
            
            out.release()
            print(f"Clip saved as {filename}")
            os.system(f"ffmpeg -y -i ./static/clip/{filename}.mp4 -c:v libx264 -crf 0 ./static/clip/{filename}_h264.mp4")

    def stop(self):
        self.cap.release()

def clipGroup():
    print("Waiting for ClipManager...")
    clip_managers = {}
    location_data = read_with_cctv()
    for location in location_data:
        print("Starting ClipManager,", location)
        clip_managers[location[1]] = ClipManager(location[4])
    print("Starting Server...")
    return clip_managers

