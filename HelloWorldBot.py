
# -*- coding: utf-8 -*-
from flask import Flask, request
import requests
import json
import traceback
import random
app = Flask(__name__)
import get_bot_response
import interaction
import os

token = "EAAYjhMlXP5sBANBEO37oLdsEWzr8Npv1lKf8Lnwuc19iiZApEj2XOiJNnAchpHoCdrasLnAE3MgN3Wc7xwZACwVPZB0FojsPKtZA4VdwT0U02CBIjqbCyfdGZAnz8mWg8JNm1f8a8jm9t9Y2Yx82qgq1uKaL7lcZChydW7iEfGPQZDZD"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'POST':
    try:
      data = json.loads(request.data)
      text = data['entry'][0]['messaging'][0]['message']['text'] # Incoming Message Text
      print text
      text=text.lower().replace("?","").replace(".","")
      text=text.lower()
      sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
      payload = {'recipient': {'id': sender}}
      resp=interaction.get_bot_response(text,"chepix")
      """resp=resp.split("!!")
      if len(resp)==2:#special case, saying hi
          resp=resp[0]
          message= {'text':resp}
          payload["message"]=message
          get_bot_response.save_list(os.path.realpath("./string_cache/semantic.pkl"),['','','',''],)
          r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it
          message=get_bot_response.get_response(text)
          print "holi"
          payload["message"]=message

          r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it
          print "holi"
          return "Hello world"
"""

      if resp == "[ERR: No reply matched]":#when not pre processed answe let bot decide
          message=get_bot_response.get_response(text)
          payload["message"]=message
      else:#whe preprocessed
          message= {'text':resp}
          payload["message"]=message
          get_bot_response.save_list(os.path.realpath("./string_cache/semantic.pkl"),['','','',''])
      print "holi"
      r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it
      print "holi2"
    except Exception as e:
      print traceback.format_exc() # something went wrong
  elif request.method == 'GET': # For the initial verification
    print request.args.get('hub.verify_token')
    if request.args.get('hub.verify_token') == 'verify':
      return request.args.get('hub.challenge')
    return "Wrong Verify Token"
  return "Hello World" #Not Really Necessary

if __name__ == '__main__':
  app.run(debug=True)
