import os
import cv2
import uuid

def snapshot(url, data):
    try:
        save_path = "./static/snap"
        
        cap = cv2.VideoCapture(url)
        if not cap.isOpened():
            print("Error: Unable to open RTSP stream.")
            return False
        
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to read frame from RTSP stream.")
            cap.release()
            return False

        if frame is None or frame.size == 0:
            print("Error: Captured frame is empty.")
            cap.release()
            return False
        
        height, width, _ = frame.shape

        for idx in range(len(data)):
            fileId = uuid.uuid4()
            filename = f"{fileId}.png"
            save_file_path = os.path.join(save_path, filename)

            x1, y1, x2, y2 = data[idx].bbox

            x1 = max(0, min(x1, width))
            x2 = max(0, min(x2, width))
            y1 = max(0, min(y1, height))
            y2 = max(0, min(y2, height))
            
            if x1 == x2 or y1 == y2:
                print("Error: Invalid bounding box dimensions.")
                cap.release()
                return False

            cropped_image = frame[y1:y2, x1:x2]
            cv2.imwrite(save_file_path, cropped_image)
            data[idx].thumb = filename
        
        # cap.release()
        return data
    except Exception as e:
        print("Error occurred in utils.snapshot.snapshot:", e)
        return False