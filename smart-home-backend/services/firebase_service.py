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
    logs_ref = db.collection("logs").stream()
    return [doc.to_dict() for doc in logs_ref]


def create_user(username, preferences):
    db.collection("users").document(username).set(preferences)


def get_user(username):
    doc = db.collection("users").document(username).get()
    if doc.exists:
        return doc.to_dict()
    return None


def get_all_users():
    users_ref = db.collection("users").stream()
    return {doc.id: doc.to_dict() for doc in users_ref}


def apply_user_preferences(username):
    user_doc = db.collection("users").document(username).get()
    if not user_doc.exists:
        return None

    preferences = user_doc.to_dict()

    db.collection("devices").document("light").set({
        "state": preferences.get("default_light", False)
    })

    db.collection("devices").document("fan").set({
        "state": preferences.get("default_fan", False)
    })

    return preferences