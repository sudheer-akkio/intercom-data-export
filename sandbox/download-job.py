import gzip
import os

import requests

job_identifier = "2w1qdx03fsk0q41h"
url = "https://api.intercom.io/download/content/data/" + job_identifier


access_token = os.getenv("INTERCOM_ACCESS_TOKEN")

headers = {
    "Accept": "application/octet-stream",
    "Intercom-Version": "2.10",
    "Authorization": f"Bearer {access_token}",
}

response = requests.get(url, headers=headers)

# data = response.json()
# print(data)

# Check if the request was successful
if response.status_code == 200:
    # Specify the file name and path where the gzipped file will be saved
    file_path = "downloaded_data.csv.gz"

    # Open a gzip file in write binary ('wb') mode
    with gzip.open(file_path, "wb") as f:
        f.write(response.content)  # Write the binary data to a gzipped file

    print(f"File saved successfully: {file_path}")
else:
    print(f"Failed to download the file: HTTP {response.status_code}")
