import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

print("Firebase Service: Initializing...")
firebase_key = os.environ.get("FIREBASE_KEY")
if not firebase_key:
    # Try to load it if missing (sometimes uvicorn child processes lose env vars if not careful)
    try:
        with open("/Users/harshil/Documents/smart home/smart-home-backend/ServiceAccount.json", "r") as f:
            firebase_key = f.read()
            os.environ["FIREBASE_KEY"] = firebase_key
    except:
        print("Firebase Service ERROR: FIREBASE_KEY not in env and ServiceAccount.json missing")

cred_dict = json.loads(firebase_key)
cred = credentials.Certificate(cred_dict)

if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()
print("Firebase Service: DB Client connected")


def save_log(log_data):
    print(f"Firebase Service: Saving log {log_data.get('intent')}")
    db.collection("logs").add(log_data)


def update_device(device_name, state):
    print(f"Firebase Service: Updating device {device_name} to {state}")
    db.collection("devices").document(device_name).set({
        "state": state
    })


def get_all_devices():
    print("Firebase Service: Fetching all devices...")
    try:
        # Use .get() instead of .stream()
        docs = db.collection("devices").get()
        devices = {}
        for doc in docs:
            devices[doc.id] = doc.to_dict().get("state", False)
        print(f"Firebase Service: Found {len(devices)} devices")
        return devices
    except Exception as e:
        print(f"Firebase Service ERROR in get_all_devices: {e}")
        import traceback
        traceback.print_exc()
        return {}


def get_all_logs():
    print("Firebase Service: Fetching all logs...")
    try:
        # Use .get() and manual sort for now to avoid index issues if needed
        # But order_by on one field should be fine with .get()
        docs = db.collection("logs").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).get()
        logs = [doc.to_dict() for doc in docs]
        print(f"Firebase Service: Found {len(logs)} logs")
        return logs
    except Exception as e:
        print(f"Firebase Service ERROR in get_all_logs: {e}")
        # Fallback to unsorted logs if order_by fails
        print("Firebase Service: Retrying without order_by")
        docs = db.collection("logs").limit(50).get()
        return [doc.to_dict() for doc in docs]