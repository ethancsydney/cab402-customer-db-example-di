import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import random

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Add the path to your service account key JSON file
creds = ServiceAccountCredentials.from_json_keyfile_name(r'.env/google_api_key.json', scope)

# Authorize the client
client = gspread.authorize(creds)

# Open the Google Sheet by its name
sheet = client.open("Your Google Sheet Name").sheet1

# Example dummy data to insert
header = ["customer_id", "customer_email", "customer_name", "lead_generated_by_email", "lead_generated_by_name", "active_customer_flag", "last_contacted_date", "customer_cancelled_date"]
dummy_data = [
    [1, "customer1@example.com", "Customer One", "lead1@example.com", "Lead One", "Y", (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"), ""],
    [2, "customer2@example.com", "Customer Two", "lead2@example.com", "Lead Two", "N", (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"), (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d")],
    [3, "customer3@example.com", "Customer Three", "lead3@example.com", "Lead Three", "Y", (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"), ""],
    [4, "customer4@example.com", "Customer Four", "lead4@example.com", "Lead Four", "Y", (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"), ""],
    [5, "customer5@example.com", "Customer Five", "lead5@example.com", "Lead Five", "N", (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"), (datetime.now() - timedelta(days=random.randint(1, 10))).strftime("%Y-%m-%d")],
    [6, "customer6@example.com", "Customer Six", "lead6@example.com", "Lead Six", "Y", (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"), ""]
]

# Clear existing content
sheet.clear()

# Insert the header
sheet.append_row(header)

# Insert the dummy data
for row in dummy_data:
    sheet.append_row(row)

print("Dummy data has been added to the Google Sheet.")
