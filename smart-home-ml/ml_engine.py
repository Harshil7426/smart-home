import cv2
import requests
import time

BACKEND_URL = "http://localhost:8000/ml-result"

last_detected_user = None
last_enter_time = 0

def send_to_backend(user, intent, confidence=0.95):
    data = {
        "user": user,
        "intent": intent,
        "confidence": confidence
    }

    try:
        response = requests.post(BACKEND_URL, json=data)
        print("Backend Response:", response.json())
    except Exception as e:
        print("Error sending to backend:", e)


def fake_face_recognition():
    return "Harshil"


def fake_manual_intent():
    # Only manual commands alternate
    intents = ["TURN_LIGHT_ON", "TURN_LIGHT_OFF"]
    return intents[int(time.time()) % len(intents)]


def main():
    global last_detected_user, last_enter_time

    cap = cv2.VideoCapture(0)
    trigger_interval = 5

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow("Camera Feed", frame)

        current_time = time.time()
        user = fake_face_recognition()

        # 🔥 Trigger ENTER_ROOM only once when user appears
        if user != last_detected_user:
            print(f"{user} entered room")
            send_to_backend(user, "ENTER_ROOM")
            last_detected_user = user
            last_enter_time = current_time

        # 🔹 Manual commands every 5 seconds
        if current_time - last_enter_time >= trigger_interval:
            intent = fake_manual_intent()
            print(f"Detected: {user} → {intent}")
            send_to_backend(user, intent)
            last_enter_time = current_time

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()