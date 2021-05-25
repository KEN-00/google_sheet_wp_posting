from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google import sheethelper
from wp import postcreater
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


if __name__ == '__main__':
    serviceAccountInfo = get_service_account_info()
    googleSheetConfig = get_google_sheet_config()

    spreadSheetID = None
    queryRange = None
    scopes = None

    ## get google sheet information and API params from configuration
    try:
        spreadSheetID = googleSheetConfig['spreadSheetID']
        queryRange = googleSheetConfig['queryRange']
        scopes = googleSheetConfig['scopes']
    except KeyError as k:
        print ('google sheet config {} is missing, please set {} in {}'.format(k, k, SHEET_CONFIG_FILE_NAME))
        exit()


    data = sheethelper.get_formatted_sheet_data(serviceAccountInfo, spreadSheetID, queryRange, scopes)
    
    if data:
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

        for datum in data:
            postcreater.create_post(
                apiUserName=wpApiUserName,
                apiPassword=wpApiPassword,
                authorID=authorID,
                categories=categories,
                postEndPointURL=wpPostEndPointURL,
                postStatus=postStatus,
                postData=datum                
            )




