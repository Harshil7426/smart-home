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