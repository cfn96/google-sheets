# This script reads data from a Google Sheet using the gspread library.
# The gspread library needs to be installed first. You can do this by running:
# pip install gspread google-auth

import gspread
from google.oauth2.service_account import Credentials
import json

# =========================================================================
# === IMPORTANT: SETUP INSTRUCTIONS BEFORE YOU RUN THIS SCRIPT ===
# =========================================================================
# 1. Go to the Google Cloud Console (https://console.cloud.google.com/)
# 2. Create a new project or select an existing one.
# 3. Enable the "Google Sheets API" for your project.
# 4. Go to "APIs & Services" -> "Credentials".
# 5. Click "Create Credentials" -> "Service Account".
# 6. Give the service account a name and role (e.g., "Viewer" is sufficient).
# 7. Create a new JSON key for the service account and download it.
# 8. Rename the downloaded file to 'credentials.json' and place it in the same directory as this script.
# 9. Get the email address of your service account (e.g., my-service-account@my-project-1234.iam.gserviceaccount.com).
# 10. Open your Google Sheet, click "Share", and invite the service account email with "Editor" permissions.
# 11. Replace the placeholder values for 'SPREADSHEET_ID' and 'WORKSHEET_NAME' below.

# The path to your service account credentials file.
# You must have followed the setup steps above for this to work.
CREDENTIALS_FILE = './credentials.json'

# Replace with the ID of your Google Sheet.
# You can find the spreadsheet ID in the URL:
# https://docs.google.com/spreadsheets/d/{your_spreadsheet_id_goes_here}/edit
SPREADSHEET_ID = '19o6daH5dkhwr1bCdKHEKcnH-EylgNJaFy-q76wyZMns'

# Replace with the name of the worksheet (e.g., 'Sheet1', 'Data').
WORKSHEET_NAME = 'Sheet1'

def read_google_sheet():
    """
    Authenticates with the Google Sheets API and reads all data from a worksheet.
    """
    try:
        # Load credentials from the JSON file.
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(
            CREDENTIALS_FILE, scopes=scope)

        # Authorize the gspread client.
        gc = gspread.authorize(creds)

        print("Authentication successful!")

        # Open the specified spreadsheet and worksheet.
        sheet = gc.open_by_key(SPREADSHEET_ID)
        worksheet = sheet.worksheet(WORKSHEET_NAME)

        print(f"Reading data from worksheet '{worksheet.title}'...")

        # Get all records from the worksheet as a list of dictionaries.
        # This is a good way to get data if your sheet has a header row.
        # For example, a row like ['name': 'John', 'age': 30]
        data = worksheet.get_all_records()

        # You can also get all values as a list of lists.
        # all_values = worksheet.get_all_values()

        # Check if any data was found.
        if data:
            print("\nData found:")
            # Iterate through the rows and print them.
            # 'row' will be a dictionary for each record.
            for row in data:
                # Use json.dumps to print the dictionary in a readable format.
                print(json.dumps(row, indent=2))
        else:
            print("No data found in the worksheet.")

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet with ID '{SPREADSHEET_ID}' not found.")
        print("Please double-check the ID and ensure the service account has access.")
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Worksheet named '{WORKSHEET_NAME}' not found.")
        print("Please double-check the worksheet name.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please check your credentials.json file and internet connection.")

# Call the function to run the script.
if __name__ == "__main__":
    read_google_sheet()
