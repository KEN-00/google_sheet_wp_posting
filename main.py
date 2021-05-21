from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import io
import json

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_RANGE_NAME = 'A1:B2'
SHEET_CONFIG_FILE_NAME = 'google_sheet_config.json'
CREDENTIALS_FILE_NAME = 'credentials.json'

def main(credentialsData, googleSheetConfig):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                credentialsData, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    print(sheet.values())

    spreadSheetID = googleSheetConfig['spreadSheetID']
    range = googleSheetConfig['range']

    if not spreadSheetID or not range:
        print('spreadSheetID/range is not set properly')

    result = sheet.values().get(spreadsheetId=spreadSheetID,
                                range=range).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print(row)
            print('%s, %s' % (row[0], row[1]))


def get_credentials():
    return get_json_data(CREDENTIALS_FILE_NAME)

def get_google_sheet_config():
    return get_json_data(SHEET_CONFIG_FILE_NAME)

def get_json_data(filename): 
    with io.open(filename, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data          

if __name__ == '__main__':
    credentialsData = get_credentials()
    googleSheetConfig = get_google_sheet_config()
    main(credentialsData, googleSheetConfig)