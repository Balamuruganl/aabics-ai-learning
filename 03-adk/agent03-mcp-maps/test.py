
from pathlib import Path
import os
import json
import requests
from dotenv import load_dotenv

load_dotenv(Path(".env").resolve())
api_key = os.getenv("MAPS_API_KEY")

payload = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "compute_routes",
        "arguments": {
            "origin": {"address": "London, UK"},
            "destination": {"address": "Manchester, UK"},
            "travelMode": "DRIVE"
        }
    }
}

response = requests.post(
    "https://mapstools.googleapis.com/mcp",
    headers={
        "X-Goog-Api-Key": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    },
    json=payload,
    timeout=60,
)

print("HTTP status:", response.status_code)
print(response.text)
