from datetime import datetime
from services.firebase_service import (
    save_log,
    update_device,
    get_all_devices,
    apply_user_preferences,
    get_user,
    get_all_logs
)

def process_ml_result(data):
    if data.intent == "TURN_LIGHT_ON":
        update_device("light", True)
    elif data.intent == "TURN_LIGHT_OFF":
        update_device("light", False)

    log_entry = {
        "intent": data.intent,
        "confidence": data.confidence,
        "timestamp": datetime.now().isoformat()
    }

    save_log(log_entry)

    return get_all_devices()


# 🔥 ADD THESE (THEY WERE MISSING)

def get_devices():
    return get_all_devices()


def manual_device_control(device, state):
    update_device(device, state)
    return get_all_devices()


def get_logs():
    return get_all_logs()