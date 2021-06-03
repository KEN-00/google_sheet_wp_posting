

# google_sheet_wp_posting
A Python util that create WordPress posts with Google Sheet data (TBC)

## Google Cloud Prerequisite
1. Create a Google account.

2. Create a Google Cloud project and enable Google Sheets API in the Google Cloud Console (see [https://developers.google.com/workspace/guides/create-project](https://developers.google.com/workspace/guides/create-project)).

3. Create a service account and a JSON key, download the service account's JSON key file to the project directory  and rename the file to "service_account_info.json" (see [https://developers.google.com/identity/protocols/oauth2/service-account](https://developers.google.com/identity/protocols/oauth2/service-account)).

## Setup
To install dependencies:
`pip install -r requirements.txt`

  ### Environment Variables
A set of environment variables define the file paths of the configuration files required by the system:
| Environment Variable| Default Value   | 
| ------------ | ------------ | 
| GOOGLE_SHEET_CONFIG_FILE_PATH |  resource/google_sheet_config.json |  
| SERVICE_ACCOUNT_INFO_FILE_PATH |  resource/service_account_info.json |  
| WP_API_CONFIG_FILE_PATH |  resource/wp_api_config.json |  
| JINJA2_POST_TEMPLATE_FILE_PATH |  resource/post_template.jinja2 |  

### Google Sheet Config
Configure the spreadsheet ID and query range in `google_sheet_config.json` 
Please see [https://developers.google.com/sheets/api/guides/concepts](https://developers.google.com/sheets/api/guides/concepts) for details.

Set the `dataTransformationMapping ` to define how to map Google Sheet column to JSON. The key of the mapping is the name of column displayed in the first row of the Google spreadsheet, while the value of the mapping is the name JSON key that the data will be mapped to. The transformed JSON data will be used to create WordPress post.

For example:

Sample spreadsheet:
| Title  | Name of Google Sheet Column 1   |  Name of Google Sheet Column 2 |
| ------------ | ------------ | ------------ |
| The title |  Column 1 Value |  Column 2 Value |



Sample `google_sheet_config.json`:
`````json
{
  "spreadSheetID": "[your Google sheet ID]",
  "queryRange": "A:ZZZ",
  "scopes": [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
  ],
  "dataTransformationMapping": {
    "Title": "title",
    "Name of Google Sheet Column 1": "googleSheetColumn1",
    "Name of Google Sheet Column 2": "googleSheetColumn2"
  }
}
`````

The transformed JSON data will look like:
`````json
{
	"title":"The title",
	"googleSheetColumn1":"Column 1 Value",
	"googleSheetColumn2":"Column 2 Value"		
}
`````

### Jinja2 Template
Create a Jinja2 template file `post_template.jinja2` for creating WordPress post with content, which can be string template or HTML template.

Sample `post_template.jinja2`:
```html
{% macro render_generic_row(itemName, itemValue) -%}
<div class="row-container">
    <tr>
        <td>{{ itemName }}</td>
        <td>:</td>
        <td>{{ itemValue }}</td>
    </tr>
</div>
{%- endmacro %}

<div class="table-container">
    <table class="table">
        {% if title %}
            {{ render_generic_row('Title', title) }}
        {% endif %}
        {% if googleSheetColumn1 %}
            {{ render_generic_row('Google Sheet Column 1', googleSheetColumn1) }}
        {% endif %}
        {% if googleSheetColumn2 %}
            {{ render_generic_row('Google Sheet Column 2', googleSheetColumn2) }}
        {% endif %}
    </table>
</div>
```
Jinja2 will render the post content with the template and the JSON data transformed from Google Sheet rows using the `dataTransformationMapping ` config.

For details, please read [Jinja official documentaion](https://jinja.palletsprojects.com/en/3.0.x/).
### WordPress Rest API Config
Generate an application password in WordPress using the [Application Passwords](https://wordpress.org/plugins/application-passwords/ "Application Passwords") plugin.

Configure the authentication info (userName and password) and WordPress REST API parameters  in `wp_api_config.json` .

Please see [https://developer.wordpress.org/rest-api/reference/posts/#create-a-post](https://developer.wordpress.org/rest-api/reference/posts/#create-a-post) for details.

Sample `wp_api_config.json`:
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
