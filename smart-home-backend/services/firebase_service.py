import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import threading

# Global Firebase objects
db = None

def initialize_firebase():
    global db
    if db is not None:
        return db

    firebase_key = os.environ.get("FIREBASE_KEY")
    if not firebase_key:
        try:
            with open("ServiceAccount.json", "r") as f:
                firebase_key = f.read()
                os.environ["FIREBASE_KEY"] = firebase_key
        except:
            return None

    try:
        cred_dict = json.loads(firebase_key)
        cred = credentials.Certificate(cred_dict)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        return db
    except:
        return None

# Initialize early
initialize_firebase()

def save_log(log_data):
    if not db: return
    # Run in background thread to avoid blocking if quota hit
    def bg_save():
        try:
            db.collection("logs").add(log_data)
        except:
            pass
    threading.Thread(target=bg_save, daemon=True).start()

def update_device(device_name, state):
    if not db: return
    def bg_update():
        try:
            db.collection("devices").document(device_name).set({"state": state})
        except:
            pass
    threading.Thread(target=bg_update, daemon=True).start()

def get_all_devices_from_db(timeout=3):
    if not db: return {}
    
    result = {}
    completed = threading.Event()

    def fetch():
        nonlocal result
        try:
            docs = db.collection("devices").get()
            result = {doc.id: doc.to_dict().get("state", False) for doc in docs}
        except:
            pass
        completed.set()

    thread = threading.Thread(target=fetch, daemon=True)
    thread.start()
    completed.wait(timeout)
    return result

def get_all_logs_from_db(timeout=3):
    if not db: return []
    
    result = []
    completed = threading.Event()

    def fetch():
        nonlocal result
        try:
            docs = db.collection("logs").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(50).get()
            result = [doc.to_dict() for doc in docs]
        except:
            pass
        completed.set()

    thread = threading.Thread(target=fetch, daemon=True)
    thread.start()
    completed.wait(timeout)
    return result