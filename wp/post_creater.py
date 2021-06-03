#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import requests
import json
from . import post_content_creater


DEFAULT_HEADERS = {'content-type': "Application/json"}
POST_TITLE_KEY = 'title'

def create_post(apiUserName, 
apiPassword, 
authorID, 
categories, 
jinja2PostTemplate,
postEndPointURL, 
postStatus, 
postData,
title):

    auth = (apiUserName, apiPassword)
    postContent = post_content_creater.create_post_content(postData, jinja2PostTemplate)
    

    payload = {
        'title': title ,
        'content' : postContent ,
        'status' : postStatus ,
        'author' : authorID ,
        'categories': categories
    }

    payloadData = json.dumps(payload)

    try:
        response = requests.post(postEndPointURL, data=payloadData , headers=DEFAULT_HEADERS, auth=auth)
        if response.ok is not True or response.status_code != 200:
            print("create post request failed, response: {}".format(json.loads(response.content)))
    except requests.exceptions.ConnectionError as err:
        print("Connection failure!!!!!!!!!!!!!!!!!!!!!!!")

def get_title(postData):
    title = None
    try:
        title = postData[POST_TITLE_KEY]
    except KeyError:
        title = ''
    return title
