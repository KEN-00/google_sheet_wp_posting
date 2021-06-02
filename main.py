from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google import sheet_helper
from wp import post_creater
import io
import json

SHEET_CONFIG_FILE_NAME = 'google_sheet_config.json'
SERVICE_ACCOUNT_INFO_FILE_NAME = 'service_account_info.json'
WP_API_CONFIG_FILE_NAME = 'wp_api_config.json'


def get_service_account_info():
    return get_json_data(SERVICE_ACCOUNT_INFO_FILE_NAME)


def get_google_sheet_config():
    return get_json_data(SHEET_CONFIG_FILE_NAME)


def get_wp_api_config():
    return get_json_data(WP_API_CONFIG_FILE_NAME)


def get_json_data(filename): 
    with io.open(filename, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data          


def main():
    serviceAccountInfo = get_service_account_info()
    googleSheetConfig = get_google_sheet_config()

    spreadSheetID = None
    queryRange = None
    scopes = None
    dataTransformationMapping = None

    ## get google sheet information and API params from configuration
    try:
        spreadSheetID = googleSheetConfig['spreadSheetID']
        queryRange = googleSheetConfig['queryRange']
        scopes = googleSheetConfig['scopes']
    except KeyError as k:
        print ('google sheet config {} is missing, please set {} in {}'.format(k, k, SHEET_CONFIG_FILE_NAME))
        exit()

    try:
        dataTransformationMapping = googleSheetConfig['dataTransformationMapping']
    except KeyError as k:
        print ('dataTransformationMapping is missing in {}, default will be used'.format(SHEET_CONFIG_FILE_NAME))    

    formattedSheetDataList = sheet_helper.get_formatted_sheet_data_list(serviceAccountInfo, spreadSheetID, queryRange, scopes)
    
    if formattedSheetDataList:
        wpApiConfig = get_wp_api_config()
        wpApiUserName = None
        wpApiPassword = None
        wpPostEndPointURL = None
        authorID = None
        categories = None
        postStatus = None

        try:
            wpApiUserName = wpApiConfig['userName']
            wpApiPassword = wpApiConfig['password']
            wpPostEndPointURL = wpApiConfig['postEndPointURL']
            authorID = wpApiConfig['authorID']
            categories = wpApiConfig['categories']
            postStatus = wpApiConfig['postStatus']

        except KeyError as k:
            print ('WordPress API config {} is missing, please set {} in {}'.format(k, k, WP_API_CONFIG_FILE_NAME))
            exit()

        for data in formattedSheetDataList:
            transformedData = sheet_helper.get_transformed_sheet_data(data, dataTransformationMapping)
            title = transformedData['title']
            
            post_creater.create_post(
                apiUserName=wpApiUserName,
                apiPassword=wpApiPassword,
                authorID=authorID,
                categories=categories,
                postEndPointURL=wpPostEndPointURL,
                postStatus=postStatus,
                postData=data,
                title=title                
            )

if __name__ == '__main__':
    main()




