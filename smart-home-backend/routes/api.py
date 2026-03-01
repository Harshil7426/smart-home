from fastapi import APIRouter
from models.schemas import MLResult, DeviceControl
from services.decision_engine import (
    process_ml_result,
    get_devices,
    manual_device_control,
    get_logs
)

router = APIRouter()

@router.get("/")
def home():
    return {"message": "Smart Home Backend Running"}

@router.post("/ml-result")
def receive_ml(data: MLResult):
    updated_devices = process_ml_result(data)
    return {"status": "processed", "devices": updated_devices}

@router.get("/devices")
def devices():
    return get_devices()

@router.post("/device-control")
def manual_control(control: DeviceControl):
    updated = manual_device_control(control.device, control.state)
    return {"status": "updated", "devices": updated}

@router.get("/logs")
def logs():
    return get_logs()


from services.firebase_service import (
    create_user,
    get_user,
    get_all_users
)

from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    default_light: bool
    default_fan: bool
    permissions: str

@router.post("/users")
def add_user(user: UserCreate):
    preferences = {
        "default_light": user.default_light,
        "default_fan": user.default_fan,
        "permissions": user.permissions
    }
    create_user(user.username, preferences)
    return {"status": "user created"}

@router.get("/users")
def list_users():
    return get_all_users()