from flask import Flask, request
import requests
import json
import traceback
import random
app = Flask(__name__)

token = "EAAYjhMlXP5sBANBEO37oLdsEWzr8Npv1lKf8Lnwuc19iiZApEj2XOiJNnAchpHoCdrasLnAE3MgN3Wc7xwZACwVPZB0FojsPKtZA4VdwT0U02CBIjqbCyfdGZAnz8mWg8JNm1f8a8jm9t9Y2Yx82qgq1uKaL7lcZChydW7iEfGPQZDZD"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
  if request.method == 'POST':
    try:
      data = json.loads(request.data)
      text = data['entry'][0]['messaging'][0]['message']['text'] # Incoming Message Text
      print text
      sender = data['entry'][0]['messaging'][0]['sender']['id'] # Sender ID
      payload = {'recipient': {'id': sender},        "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":"What do you want to do next?",
        "buttons":[
          {
            "type":"web_url",
            "title":"Show Website",
            "payload":"DEVELOPER_DEFINED_PAYLOAD"

          },
          {
            "type":"postback",
            "title":"Start Chatting",
            "payload":"DEVELOPER_DEFINED_PAYLOAD"
          }
        ]
      }
    }
  }}
      r = requests.post('https://graph.facebook.com/v2.6/me/messages/?access_token=' + token, json=payload) # Lets send it
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
