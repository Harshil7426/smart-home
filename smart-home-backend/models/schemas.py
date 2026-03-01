from pydantic import BaseModel

class MLResult(BaseModel):
    user: str
    intent: str
    confidence: float

class DeviceControl(BaseModel):
    device: str
    state: bool