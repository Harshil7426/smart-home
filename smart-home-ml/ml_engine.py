import os
import sys
from unittest.mock import MagicMock

# --- CRITICAL: MOCK MATPLOTLIB BEFORE ANY OTHER IMPORTS ---
sys.modules['matplotlib'] = MagicMock()
sys.modules['matplotlib.pyplot'] = MagicMock()
sys.modules['matplotlib.font_manager'] = MagicMock()

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import requests
import time
import threading
from flask import Flask, Response
from flask_cors import CORS

# --- Configuration ---
BACKEND_URL = "http://localhost:8000/ml-result"
STREAM_PORT = 5001
MODEL_PATH = "hand_landmarker.task"

# --- MediaPipe Tasks Setup ---
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.VIDEO,
    num_hands=1,
    min_hand_detection_confidence=0.7,
    min_hand_presence_confidence=0.5
)
landmarker = HandLandmarker.create_from_options(options)

# --- Global State ---
last_intent = None
last_intent_time = 0
current_frame = None
lock = threading.Lock()

# --- Flask Server ---
app = Flask(__name__)
CORS(app)

def generate():
    while True:
        with lock:
            if current_frame is None: continue
            (flag, img) = cv2.imencode(".jpg", current_frame)
            if not flag: continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(img) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

def run_server():
    app.run(host="0.0.0.0", port=STREAM_PORT, debug=False, threaded=True, use_reloader=False)

def send_to_backend(intent, confidence=0.95):
    try:
        requests.post(BACKEND_URL, json={"intent": intent, "confidence": confidence}, timeout=1)
    except: pass

def draw_landmarks(image, detection_result):
    if not detection_result.hand_landmarks: return
    h, w, c = image.shape
    for hand_lms in detection_result.hand_landmarks:
        for lm in hand_lms:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(image, (cx, cy), 3, (0, 242, 255), -1)

def detect_gesture(detection_result):
    if not detection_result.hand_landmarks: return None
    lms = detection_result.hand_landmarks[0]
    
    # Simple finger-up check
    # Tip IDs: Index: 8, Middle: 12, Ring: 16, Pinky: 20
    # PIP IDs: Index: 6, Middle: 10, Ring: 14, Pinky: 18
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    up = [lms[tip].y < lms[pip].y for tip, pip in zip(tips, pips)]
    
    if up[0] and up[1] and not up[2] and not up[3]: return "TURN_LIGHT_ON"
    if not any(up): return "TURN_LIGHT_OFF"
    return None

def main():
    global current_frame, last_intent, last_intent_time
    threading.Thread(target=run_server, daemon=True).start()
    cap = cv2.VideoCapture(0)
    print(f"ML Engine Started (Tasks API) on port {STREAM_PORT}...")
    send_to_backend("SYSTEM_STARTUP")

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        # Process for Tasks API
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        timestamp = int(time.time() * 1000)
        
        result = landmarker.detect_for_video(mp_image, timestamp)
        
        gesture = detect_gesture(result)
        draw_landmarks(frame, result)

        current_time = time.time()
        if gesture and gesture != last_intent:
            print(f"Gesture Change Detect: {gesture}")
            send_to_backend(gesture)
            last_intent, last_intent_time = gesture, current_time

        cv2.putText(frame, "AI VISION ACTIVE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 242, 255), 2)
        if gesture:
            cv2.putText(frame, f"GESTURE: {gesture.replace('_',' ')}", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        with lock:
            current_frame = frame.copy()
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cap.release()

if __name__ == "__main__":
    main()