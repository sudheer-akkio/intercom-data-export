import os
import time
from datetime import datetime

import requests

url = "https://api.intercom.io/export/content/data/"

access_token = os.getenv("INTERCOM_ACCESS_TOKEN")


start_date = datetime(2023, 1, 1, 0, 0, 0)
end_date = datetime(2023, 4, 1, 0, 0, 0)

payload = {
    "created_at_after": 1672614245,
    "created_at_before": 1712009045,
}

headers = {
    "Content-Type": "application/json",
    "Intercom-Version": "2.10",
    "Authorization": f"Bearer {access_token}",
}

response = requests.post(url, json=payload, headers=headers)

data = response.json()
print(data)
