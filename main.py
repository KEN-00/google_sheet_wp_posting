from __future__ import print_function
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google import sheet_helper
from wp import post_creater
import io
import json
import os


GOOGLE_SHEET_CONFIG_FILE_PATH_VAR_KEY = 'GOOGLE_SHEET_CONFIG_FILE_PATH'
SERVICE_ACCOUNT_INFO_FILE_PATH_VAR_KEY = 'SERVICE_ACCOUNT_INFO_FILE_PATH'
WP_API_CONFIG_FILE_PATH_VAR_KEY = 'WP_API_CONFIG_FILE_PATH'
JINJA2_POST_TEMPLATE_FILE_PATH_VAR_KEY ='JINJA2_POST_TEMPLATE_FILE_PATH'

DEFAULT_GOOGLE_SHEET_CONFIG_FILE_PATH = 'resource/google_sheet_config.json'
DEFAULT_SERVICE_ACCOUNT_INFO_FILE_PATH = 'resource/service_account_info.json'
DEFAULT_WP_API_CONFIG_FILE_PATH = 'resource/wp_api_config.json'
DEFAULT_JINJA2_POST_TEMPLATE_FILE_PATH = 'resource/post_template.jinja2'


def get_google_sheet_config():
    filePath = get_env_config(GOOGLE_SHEET_CONFIG_FILE_PATH_VAR_KEY, DEFAULT_GOOGLE_SHEET_CONFIG_FILE_PATH)
    return get_json_data(filePath)


def get_wp_api_config():
    filePath = get_env_config(WP_API_CONFIG_FILE_PATH_VAR_KEY, DEFAULT_WP_API_CONFIG_FILE_PATH)
    return get_json_data(filePath)


def get_service_account_info():
    filePath = get_env_config(SERVICE_ACCOUNT_INFO_FILE_PATH_VAR_KEY, DEFAULT_SERVICE_ACCOUNT_INFO_FILE_PATH)
    return get_json_data(filePath)

def get_json_data(filename): 
    with io.open(filename, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        return data          


def get_jinja2_post_template():
    filePath = get_env_config(JINJA2_POST_TEMPLATE_FILE_PATH_VAR_KEY, DEFAULT_JINJA2_POST_TEMPLATE_FILE_PATH)
    with io.open(filePath, "r") as jinja2_file:
        return jinja2_file.read()
    


def get_env_config(key, default):
    return default if not os.environ.get(key) else os.environ.get(key)


def main():
    serviceAccountInfo = get_service_account_info()
    googleSheetConfig = get_google_sheet_config()

    print(googleSheetConfig)

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
        print ('google sheet config {} is missing, please set {} in {}'.format(k, k, DEFAULT_GOOGLE_SHEET_CONFIG_FILE_PATH))
        exit()

    try:
        dataTransformationMapping = googleSheetConfig['dataTransformationMapping']
    except KeyError as k:
        print ('dataTransformationMapping is missing in {}, default will be used'.format(DEFAULT_GOOGLE_SHEET_CONFIG_FILE_PATH))    

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
            print ('WordPress API config {} is missing, please set {} in {}'.format(k, k, DEFAULT_WP_API_CONFIG_FILE_PATH))
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




