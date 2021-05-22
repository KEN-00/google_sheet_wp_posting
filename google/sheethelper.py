from google.oauth2 import service_account
from googleapiclient.discovery import build
import json

def get_formatted_sheet_data(serviceAccountInfo, spreadSheetID, queryRange, scopes):
    sheetData = []
    values = get_sheet_values(serviceAccountInfo, spreadSheetID, queryRange, scopes)

    if values:

        header = values.pop(0)
        headerLength = len(header)
        rows = values
        
        for row in rows:
            datum = {}
            for i in range(headerLength):
                column = header[i]
                value = get_list_item(row, i)

                datum[column] = value
            
            sheetData.append(datum)

    return sheetData


def get_list_item(list, index):
    item = None

    try:
        item = list[index]
    except IndexError:
        print('returning empty string as index {} is out of bound of list {}'.format(index, list))
        item = ''

    return item


def get_sheet_values(serviceAccountInfo, spreadSheetID, queryRange, scopes):
    # Call the Sheets API using discovery service
    service = build_discovery_service(serviceAccountInfo, scopes)
    sheet = service.spreadsheets()
    print(sheet.values())

    result = sheet.values().get(spreadsheetId=spreadSheetID,
                                range=queryRange).execute()
    print('result: {}'.format(json.dumps(result)))

    values = result.get('values', [])

    ## if not value is returned
    if not values:
        print('empty sheet.')
        return None
    
    ## if only one row (header) is returned, and no data row is found
    if len(values) < 2:
        print('No data rows found.')
        return None

    # Close discovery service
    service.close()

    return values


def build_discovery_service(serviceAccountInfo, scopes):
    credentials = service_account.Credentials.from_service_account_info(info=serviceAccountInfo, scopes=scopes)
    service = build('sheets', 'v4', credentials=credentials)
    return service


if __name__ == '__main__':
    fruits=['apple']
    print(get_list_item(fruits, 1))