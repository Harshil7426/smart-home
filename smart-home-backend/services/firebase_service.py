import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

firebase_key = os.environ.get("FIREBASE_KEY")

cred_dict = json.loads(firebase_key)
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)
db = firestore.client()


def save_log(log_data):
    db.collection("logs").add(log_data)


def update_device(device_name, state):
    db.collection("devices").document(device_name).set({
        "state": state
    })


def get_all_devices():
    devices_ref = db.collection("devices").stream()
    devices = {}
    for doc in devices_ref:
        devices[doc.id] = doc.to_dict().get("state", False)
    return devices


def get_all_logs():
    logs_ref = db.collection("logs").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).stream()
    return [doc.to_dict() for doc in logs_ref]