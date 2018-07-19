from flask import Flask, request
from responder import send_message
import requests

app = Flask(__name__)

FB_API_URL = 'https://graph.facebook.com/v2.6/me/messages'
VERIFY_TOKEN = 'sadasdsadasACACQWEF123124214'# <paste your verify token here>

PAGE_ACCESS_TOKEN = 'EAAYb0bBgs0EBAAnfXOI2O8umRZACyqGemo9wWgGvk9WVTgxwZBKS5tBPH0QLhgt7lRZB0yF3FLNwi3BdAdPqDXP9PXX6ZB3WnZBuplUh1pnMCiKpNdNhXWOVls9vgn2x93o9pP8FeY3DKVhGSZBfKGGIbedo0dAc2GAu5NAmk1T8WfrqZCtyrVu'# paste your page access token here>"

def send_message(recipient_id, text):
    """Send a response to Facebook"""
    payload = {
        'message': {
            'text': text
        },
        'recipient': {
            'id': recipient_id
        },
        'notification_type': 'regular'
    }

    auth = {
        'access_token': PAGE_ACCESS_TOKEN
    }

    response = requests.post(
        FB_API_URL,
        params=auth,
        json=payload
    )

    return response.json()

def get_bot_response(message):
    """This is just a dummy function, returning a variation of what
    the user said. Replace this function with one connected to chatbot."""
    return "This is a dummy response to '{}'".format(message)


def verify_webhook(req):
    if req.args.get("hub.verify_token") == VERIFY_TOKEN:
        return req.args.get("hub.challenge")
        print("webhook work")
    else:
        return "incorrect"

def respond(sender, message):
    """Formulate a response to the user and
    pass it on to a function that sends it."""
    response = get_bot_response(message)
    send_message(sender, response)


def is_user_message(message):
    """Check if the message is a message from the user"""
    return (message.get('message') and
            message['message'].get('text') and
            not message['message'].get("is_echo"))


@app.route("/webhook", methods=['GET','POST'])
def listen():
    """This is the main function flask uses to 
    listen at the `/webhook` endpoint"""
    if request.method == 'GET':
        return verify_webhook(request)

    if request.method == 'POST':
        print "masuk method post"
        payload = request.json
        event = payload['entry'][0]['messaging']
        print payload
        print event
        for x in event:
            if is_user_message(x):
                text = x['message']['text']
                sender_id = x['sender']['id']
                respond(sender_id, text)

        return "ok"