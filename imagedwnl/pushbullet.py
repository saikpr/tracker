import requests
import time
import json
import requests_toolbelt.adapters.appengine
import logging

# Use the App Engine Requests adapter. This makes sure that Requests uses
# URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()




def push_to_pushbullet(data_dict,title_text,body_text,forum_url=None):
    #HTTP headers to be send
    headers ={
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0",
              "Access-Token":data_dict["push_bullet_token"],
              "Content-Type": "application/json",
             }
    #getting the URL where the push bullet post request is to be made
    url =data_dict["push_bullet_url"]
    #JSON body of the request to be made
    body ={"body":body_text,"title":title_text,"type":"note"}
    #making the request
    req = requests.post(url,data=json.dumps(body),headers = headers)
    return True
