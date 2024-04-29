import csv
import json
import os

import requests


class IntercomExporter:

    def __init__(self, access_token):
        self._access_token = access_token  # Use a private variable to store the token
        self.headers = {
            "Intercom-Version": "2.10",
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.query = {}
        self.url = "https://api.intercom.io/"
        self.companies = []
        self.conversations = []
        self.contacts = []

    def fetch_company_data(self):
        """Fetch all pages of data from a specific Intercom endpoint"""
        endpoint = "companies"
        url = f"{self.url}{endpoint}"
        next_page = url
        starting_after = None

        query = {"per_page": "20", "starting_after": starting_after}

        while next_page:
            response = requests.get(url, headers=self.headers, params=query)
            data = response.json()
            self.companies.extend(data.get("data", []))
            # Check if there's a next page
            next_page = data.get("pages", {}).get("next")
            if next_page:
                query["starting_after"] = next_page["starting_after"]

    def fetch_conversation_data(self, write_location=""):

        endpoint = "conversations"
        url = f"{self.url}{endpoint}"
        next_page = url
        starting_after = None
        page_num = 1
        total_pages = None

        query = {"per_page": "150", "starting_after": starting_after}

        while next_page:
            print("Initializing request...")
            response = requests.get(url, headers=self.headers, params=query)
            data = response.json()
            if not total_pages:
                total_pages = data["pages"]["total_pages"]
            print(f"Starting process for page {page_num} out of {total_pages}")
            if "conversations" in data:
                print("Fetching all conversations by ID...")
                cids = [conv["id"] for conv in data["conversations"]]
                conversations = [self._fetch_conversation_by_id(cid) for cid in cids]
                self.conversations.extend(conversations)
            # Check if there's a next page
            next_page = data.get("pages", {}).get("next")
            if next_page:
                query["starting_after"] = next_page["starting_after"]

            if write_location:
                fname = os.path.join(
                    write_location, f"conversations_page_{page_num}.json"
                )
                print(f"Saving to {fname}")
                IntercomExporter.save_to_json(conversations, fname)
            print(f"Page {page_num} processing completed!")
            page_num += 1

    def fetch_contacts_data(self):

        endpoint = "contacts"
        url = f"{self.url}{endpoint}"
        next_page = url
        starting_after = None
        page_num = 1
        total_pages = None

        query = {"per_page": "20", "starting_after": starting_after}

        while next_page:
            print("Initializing request...")
            response = requests.get(url, headers=self.headers, params=query)
            data = response.json()
            if not total_pages:
                total_pages = data["pages"]["total_pages"]
            print(f"Starting process for page {page_num} out of {total_pages}")
            self.contacts.extend(data.get("data", []))
            # Check if there's a next page
            next_page = data.get("pages", {}).get("next")
            if next_page:
                query["starting_after"] = next_page["starting_after"]
            print(f"Page {page_num} processing completed!")
            page_num += 1

    # Private Methods
    def _fetch_conversation_by_id(self, cid):

        endpoint = "conversations"
        url = f"{self.url}{endpoint}/" + cid

        query = {"display_as": "plaintext"}

        response = requests.get(url, headers=self.headers, params=query)

        data = response.json()

        return data

    @staticmethod
    def save_to_json(items, filename):
        """Save data to a JSON file."""
        try:
            with open(filename, "w") as file:
                json.dump(items, file, indent=4)
            print(f"Data successfully saved to {filename}.")
        except IOError as e:
            print(f"Failed to save data: {e}")

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, value):
        self._access_token = value
        self.headers["Authorization"] = f"Bearer {self._access_token}"
