from google.oauth2 import service_account
from googleapiclient.discovery import build
import json
from . import data_getter


def get_transformed_sheet_data(sheetData, dataTransformationMapping):
    if not dataTransformationMapping:
        return sheetData

    transformedSheetData = {}

    for columnName,cellValue in sheetData.items():
        dataKey = data_getter.get_value_from_dict(dataTransformationMapping, columnName, None)
        if dataKey:
            transformedSheetData[dataKey] = cellValue


    return transformedSheetData

def get_formatted_sheet_data_list(serviceAccountInfo, spreadSheetID, queryRange, scopes):
    sheetDataList = []
    values = get_sheet_values(serviceAccountInfo, spreadSheetID, queryRange, scopes)

    if values:

        header = values.pop(0)
        headerLength = len(header)
        rows = values
        
        for row in rows:
            data = {}
            for i in range(headerLength):
                column = header[i]
                value = data_getter.get_list_item(row, i, '')

                data[column] = value
            
            sheetDataList.append(data)

    return sheetDataList


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
    arr = ['1','2','3']
    print(valuegetter.get_list_item(arr,4))
    pass