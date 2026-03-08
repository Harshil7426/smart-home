import cv2
import mediapipe as mp
import requests
import time
import threading
from flask import Flask, Response
from flask_cors import CORS

# --- Configuration ---
BACKEND_URL = "https://smart-home-4b7r.onrender.com/ml-result"
STREAM_PORT = 5001

# --- MediaPipe Setup ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# --- Global State ---
last_detected_user = "Harshil" # Mocked user for now
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
            if current_frame is None:
                continue
            (flag, encodedImage) = cv2.imencode(".jpg", current_frame)
            if not flag:
                continue
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
               bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
def video_feed():
    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

def run_server():
    app.run(host="0.0.0.0", port=STREAM_PORT, debug=False, threaded=True, use_reloader=False)

# --- Helper Functions ---
def send_to_backend(user, intent, confidence=0.95):
    data = {
        "user": user,
        "intent": intent,
        "confidence": confidence
    }
    try:
        requests.post(BACKEND_URL, json=data, timeout=2)
    except Exception as e:
        print(f"Error sending to backend: {e}")

def detect_gesture(hand_landmarks):
    # Tip IDs: Thumb: 4, Index: 8, Middle: 12, Ring: 16, Pinky: 20
    # PIP IDs: Index: 6, Middle: 10, Ring: 14, Pinky: 18
    
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    
    # Check which fingers are up
    up_fingers = []
    for tip, pip in zip(tips, pips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            up_fingers.append(True)
        else:
            up_fingers.append(False)
            
    # GESTURE 1: TWO FINGERS (Index and Middle)
    if up_fingers[0] and up_fingers[1] and not up_fingers[2] and not up_fingers[3]:
        return "TURN_LIGHT_ON"
        
    # GESTURE 2: FIST (All fingers down)
    if not any(up_fingers):
        return "TURN_LIGHT_OFF"
        
    return None

def main():
    global current_frame, last_intent, last_intent_time
    
    # Start stream server in background
    threading.Thread(target=run_server, daemon=True).start()
    
    cap = cv2.VideoCapture(0)
    print(f"ML Engine Started. Streaming on port {STREAM_PORT}...")

    # Wait for first room entry mock
    send_to_backend(last_detected_user, "ENTER_ROOM")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Process frame for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        gesture = None
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks for visual feedback in the stream
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Detect gesture
                gesture = detect_gesture(hand_landmarks)

        # Rate limit backend calls to once every 3 seconds for the same gesture
        current_time = time.time()
        if gesture and (gesture != last_intent or current_time - last_intent_time > 3):
            print(f"Gesture detected: {gesture}")
            send_to_backend(last_detected_user, gesture)
            last_intent = gesture
            last_intent_time = current_time

        # Overlay info on frame
        cv2.putText(frame, f"USER: {last_detected_user}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 242, 255), 2)
        if gesture:
            cv2.putText(frame, f"GESTURE: {gesture}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Update global frame for streaming
        with lock:
            current_frame = frame.copy()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()