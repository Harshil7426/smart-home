from datetime import datetime
from services.firebase_service import (
    save_log,
    update_device,
    get_all_devices_from_db,
    get_all_logs_from_db
)

# --- In-Memory State ---
STATE = {"light": False}
LOG_BUFFER = []

def initialize_engine():
    global STATE, LOG_BUFFER
    print("Decision Engine: Syncing with Firestore...")
    db_devices = get_all_devices_from_db()
    if db_devices:
        STATE.update(db_devices)
    
    db_logs = get_all_logs_from_db()
    if db_logs:
        LOG_BUFFER = db_logs
    print(f"Decision Engine: Sync complete. Devices: {list(STATE.keys())}, Logs: {len(LOG_BUFFER)}")

# Initial sync
initialize_engine()

def process_ml_result(data):
    global LOG_BUFFER
    
    # Only log and update if there's a state change or it's a system startup
    is_startup = data.intent == "SYSTEM_STARTUP"
    state_changed = False

    if data.intent == "TURN_LIGHT_ON":
        if not STATE["light"]:
            STATE["light"] = True
            update_device("light", True)
            state_changed = True
    elif data.intent == "TURN_LIGHT_OFF":
        if STATE["light"]:
            STATE["light"] = False
            update_device("light", False)
            state_changed = True

    if not state_changed and not is_startup:
        return STATE

    log_entry = {
        "intent": data.intent,
        "confidence": data.confidence,
        "timestamp": datetime.now().isoformat()
    }

    # Update memory immediately
    LOG_BUFFER.insert(0, log_entry)
    LOG_BUFFER = LOG_BUFFER[:50] # Keep last 50
    
    save_log(log_entry) # Background/Try-except save

    return STATE

def get_devices():
    return STATE

def manual_device_control(device, state):
    STATE[device] = state
    update_device(device, state)
    
    log_entry = {
        "intent": f"MANUAL_{device.upper()}_{'ON' if state else 'OFF'}",
        "confidence": 1.0,
        "timestamp": datetime.now().isoformat()
    }
    LOG_BUFFER.insert(0, log_entry)
    LOG_BUFFER = LOG_BUFFER[:50]
    save_log(log_entry)
    
    return STATE

def get_logs():
    return LOG_BUFFER