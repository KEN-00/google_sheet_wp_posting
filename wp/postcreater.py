#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import requests
import json
from . import content


DEFAULT_HEADERS = {'content-type': "Application/json"}


def create_post(apiUserName, 
apiPassword, 
authorID, 
categories, 
postEndPointURL, 
postStatus, 
postData):

    auth = (apiUserName, apiPassword)
    title = postData['Title']
    postContent = content.create_post_content(postData)
    

    payload = {
        'title': title ,
        'content' : postContent ,
        'status' : postStatus ,
        'author' : authorID ,
        'categories': categories
    }

    payloadData = json.dumps(payload)

    response = requests.post(postEndPointURL, data=payloadData , headers=DEFAULT_HEADERS, auth=auth)
    if response.ok is not True or response.status_code != 200:
        print("create post request failed, response: {}".format(json.loads(response.content)))