# google_sheet_wp_posting
A Python util that create WordPress posts with Google Sheet data (TBC)

## Google Cloud Prerequisite
1. Create a Google account.

2. Create a Google Cloud project and enable Google Sheets API in the Google Cloud Console (see [https://developers.google.com/workspace/guides/create-project](https://developers.google.com/workspace/guides/create-project)).

3. Create a service account and a JSON key, download the service account's JSON key file to the project directory  and rename the file to "service_account_info.json" (see [https://developers.google.com/identity/protocols/oauth2/service-account](https://developers.google.com/identity/protocols/oauth2/service-account)).

## Setup
### Google Sheet Config
Configure the spreadsheet ID and query range in `google_sheet_config.json ` 
(see [https://developers.google.com/sheets/api/guides/concepts](https://developers.google.com/sheets/api/guides/concepts)).

Sample:
`````json
{
    "spreadSheetID":"[your Google sheet ID]",
    "queryRange":"A:ZZZ",
    "scopes":[
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
}    
`````
### WordPress Rest API Config
Generate an application password in WordPress using the [Application Passwords](https://wordpress.org/plugins/application-passwords/ "Application Passwords") plugin.

Configure the authentication info (userName and password) and WordPress REST API parameters  in `wp_api_config.json `  (see [https://developer.wordpress.org/rest-api/reference/posts/#create-a-post](https://developer.wordpress.org/rest-api/reference/posts/#create-a-post) for details).

Sample:
````json
{
    "userName": "[your user name]",
    "password": "[your password]",
    "postEndPointURL": "http://localhost/wordpress/wp-json/wp/v2/posts",
    "authorID":1,
    "categories":[1],
    "postStatus":"publish"
}
````

### Execution
`python ./main.py`
