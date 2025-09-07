# This script reads data from a Google Sheet and exports it to a formatted PDF.

import gspread
from google.oauth2.service_account import Credentials
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import os

# =========================================================================
# === IMPORTANT: SETUP INSTRUCTIONS BEFORE YOU RUN THIS SCRIPT ===
# =========================================================================
# 1. Ensure you have followed all previous steps:
#    - Created a virtual environment and activated it.
#    - Installed 'gspread' and 'google-auth'.
#    - Placed your 'credentials.json' file in this directory.
#    - Shared your Google Sheet with the service account.
# 2. You need to install the 'reportlab' library for PDF generation.
#    - Run this command in your active virtual environment: pip install reportlab
# 3. Replace the placeholder values for SPREADSHEET_ID and WORKSHEET_NAME below.

# The path to your service account credentials file.
CREDENTIALS_FILE = 'credentials.json'

# Replace with the ID of your Google Sheet.
# You can find the spreadsheet ID in the URL.
SPREADSHEET_ID = '19o6daH5dkhwr1bCdKHEKcnH-EylgNJaFy-q76wyZMns'

# Replace with the name of the worksheet (e.g., 'Sheet1', 'Data').
WORKSHEET_NAME = 'Sheet1'

def export_to_pdf(data, filename="google_sheet_data.pdf"):
    """
    Exports a list of dictionaries to a formatted PDF file.
    """
    try:
        # Create a new PDF document.
        doc = SimpleDocTemplate(filename, pagesize=letter)
        
        # A list to hold the elements to be added to the PDF.
        elements = []
        
        # Get standard styles from ReportLab.
        styles = getSampleStyleSheet()
        
        # Define a custom style for the title.
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            alignment=TA_CENTER
        )
        
        # Define a style for the data paragraphs.
        data_style = ParagraphStyle(
            'DataStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=12,
        )

        # Add a title to the PDF.
        elements.append(Paragraph("Google Sheet Data Report", title_style))
        elements.append(Spacer(1, 12))
        
        # Check if there is data to write.
        if not data:
            elements.append(Paragraph("No data found to export.", data_style))
        else:
            # Iterate through each record (row) in the data.
            for i, record in enumerate(data):
                # Start a new paragraph for each record.
                elements.append(Paragraph(f"<b>Record {i+1}:</b>", styles['Normal']))
                elements.append(Spacer(1, 6))

                # Format the record's key-value pairs.
                record_text = ""
                for key, value in record.items():
                    # Create a string for each key-value pair.
                    record_text += f"<b>{key}:</b> {value}<br/>"
                
                elements.append(Paragraph(record_text, data_style))
                elements.append(Spacer(1, 12)) # Add a space between records.

        # Build the PDF file with all the elements.
        doc.build(elements)
        print(f"Successfully exported data to '{os.path.abspath(filename)}'")

    except Exception as e:
        print(f"An error occurred while creating the PDF: {e}")
        print("Please ensure your data is a list of dictionaries and reportlab is installed correctly.")


def read_google_sheet():
    """
    Authenticates with the Google Sheets API and reads all data from a worksheet.
    Then, it calls the export_to_pdf function.
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
        data = worksheet.get_all_records()
        
        # Check if any data was found and print it.
        if data:
            print("\nData found:")
            for row in data:
                print(json.dumps(row, indent=2))
            
            # Call the PDF export function with the data.
            export_to_pdf(data)
        else:
            print("No data found in the worksheet.")
            # Still call the function to create an empty PDF with a message.
            export_to_pdf(data)

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Error: Spreadsheet with ID '{SPREADSHEET_ID}' not found.")
        print("Please double-check the ID and ensure the service account has access.")
    except gspread.exceptions.WorksheetNotFound:
        print(f"Error: Worksheet named '{WORKSHEET_NAME}' not found.")
        print("Please double-check the worksheet name.")
    except FileNotFoundError:
        print("Error: The 'credentials.json' file was not found.")
        print("Please make sure it's in the same directory as the script.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please check your credentials.json file and internet connection.")

# Call the function to run the script.
if __name__ == "__main__":
    read_google_sheet()
