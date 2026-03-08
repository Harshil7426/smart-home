import os
import json

# Load ServiceAccount.json and set FIREBASE_KEY env var BEFORE imports
with open("ServiceAccount.json", "r") as f:
    cert = f.read()
    os.environ["FIREBASE_KEY"] = cert

import uvicorn
from main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
