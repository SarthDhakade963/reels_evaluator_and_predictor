import cv2
import tempfile
import os

def extract_frames(video_bytes, target_fps=1):
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as temp:
        temp.write(video_bytes)
        temp_filename = temp.name

    cap = cv2.VideoCapture(temp_filename)
    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps / target_fps) if fps > 0 else 30

    frames = []
    idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if idx % interval == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(rgb)
        idx += 1

    cap.release()
    os.unlink(temp_filename)
    return frames
