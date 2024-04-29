import csv
import json
import os

import requests

# Constants
URL = "https://api.intercom.io/conversations"

TOKEN = os.getenv(
    "INTERCOM_ACCESS_TOKEN"
)  # Replace <YOUR_TOKEN_HERE> with your actual Intercom API token
HEADERS = {"Intercom-Version": "2.10", "Authorization": f"Bearer {TOKEN}"}
MAX_CONVERSATIONS_PER_FILE = 1000


def fetch_conversations():
    conversations = []
    file_count = 0
    starting_after = None

    while True:
        query = {"per_page": "150", "starting_after": starting_after}
        response = requests.get(URL, headers=HEADERS, params=query)
        response_data = response.json()

        if "conversations" in response_data:
            conversations.extend(response_data["conversations"])
            if len(conversations) >= MAX_CONVERSATIONS_PER_FILE:
                save_as_json(conversations, f"conversations_{file_count}.json")
                save_as_csv(conversations, f"conversations_{file_count}.csv")
                file_count += 1
                conversations = []  # Reset the list for the next file

            if "next" in response_data["pages"] and response_data["pages"]["next"]:
                starting_after = response_data["pages"]["next"]["starting_after"]
            else:
                break
        else:
            break

    # Save any remaining conversations
    if conversations:
        save_as_json(conversations, f"conversations_{file_count}.json")
        save_as_csv(conversations, f"conversations_{file_count}.csv")


def save_as_json(conversations, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(conversations, f, ensure_ascii=False, indent=4)


def save_as_csv(conversations, filename):
    keys = conversations[0].keys() if conversations else []
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for conversation in conversations:
            writer.writerow(conversation)


def main():
    fetch_conversations()


if __name__ == "__main__":
    main()
