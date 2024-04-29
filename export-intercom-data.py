# Setup
import os
import sys

sys.path.append(os.path.join(os.getcwd(), "src"))

from src import intercom_utils

access_token = os.getenv("INTERCOM_ACCESS_TOKEN")

exporter = intercom_utils.IntercomExporter(access_token)

# exporter.fetch_company_data()

# exporter.save_as_csv("companies", "companies.csv")

# exporter.fetch_conversation_data(write_location=os.path.join(os.getcwd(), "data"))

# exporter.save_as_csv("conversations")

exporter.fetch_contacts_data()

fname = os.path.join(os.getcwd(), "data", "intercom_contacts.json")
intercom_utils.IntercomExporter.save_to_json(exporter.contacts, fname)
