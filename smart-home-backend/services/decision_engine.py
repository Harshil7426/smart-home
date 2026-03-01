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

    # 1️⃣ Auto apply preferences
    if data.intent == "ENTER_ROOM":
        prefs = apply_user_preferences(data.user)

        log_entry = {
            "user": data.user,
            "intent": "AUTO_APPLY_PREFERENCES",
            "confidence": data.confidence,
            "timestamp": datetime.now().isoformat()
        }

        save_log(log_entry)
        return get_all_devices()

    # 2️⃣ Manual intent processing
    user_data = get_user(data.user)

    if not user_data:
        return {"error": "User not found"}

    if user_data.get("permissions") != "full":
        return {"error": "User does not have permission"}

    if data.intent == "TURN_LIGHT_ON":
        update_device("light", True)
    elif data.intent == "TURN_LIGHT_OFF":
        update_device("light", False)
    elif data.intent == "FAN_ON":
        update_device("fan", True)
    elif data.intent == "FAN_OFF":
        update_device("fan", False)

    log_entry = {
        "user": data.user,
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