from pydantic import BaseModel

class MLResult(BaseModel):
    intent: str
    confidence: float

class DeviceControl(BaseModel):
    device: str
    state: bool