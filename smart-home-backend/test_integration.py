import os
import sys

# Set path to include current dir for absolute imports
sys.path.append(os.getcwd())

import json
import firebase_admin
from firebase_admin import credentials, firestore

print("Direct Test: Loading ServiceAccount.json")
try:
    with open("ServiceAccount.json", "r") as f:
        cert = f.read()
        os.environ["FIREBASE_KEY"] = cert
    print("Direct Test: FIREBASE_KEY set")
except Exception as e:
    print(f"Direct Test ERROR: {e}")
    exit(1)

print("Direct Test: Importing firebase_service")
try:
    from services.firebase_service import get_all_devices_from_db as get_all_devices, get_all_logs_from_db as get_all_logs
    print("Direct Test: firebase_service imported")
except Exception as e:
    print(f"Direct Test ERROR during import: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("Direct Test: Calling get_all_devices()")
try:
    devices = get_all_devices()
    print(f"Direct Test: Result: {devices}")
except Exception as e:
    print(f"Direct Test ERROR calling get_all_devices: {e}")

print("Direct Test: Calling get_all_logs()")
try:
    logs = get_all_logs()
    print(f"Direct Test: Result found {len(logs)} logs")
except Exception as e:
    print(f"Direct Test ERROR calling get_all_logs: {e}")
