import os

import requests

job_identifier = "2w1qdx03fsk0q41h"
url = "https://api.intercom.io/export/content/data/" + job_identifier

access_token = os.getenv("INTERCOM_ACCESS_TOKEN")

headers = {
    "Intercom-Version": "2.10",
    "Authorization": f"Bearer {access_token}",
}

response = requests.get(url, headers=headers)

data = response.json()
print(data)
