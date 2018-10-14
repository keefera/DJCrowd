from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import MessagingResponse
from threading import Timer
import requests

import spotifyController

DELIMITER = "::"

REFRESHCODE = "BLAH"
ACCESSCODE = ""

app = Flask(__name__)

def getNewToken():
    r = requests.post(url = "http://localhost:8888/refresh_token", data = {'refresh_token' : REFRESHCODE})
    print(r)
    t = Timer(10, getNewToken)
    t.start()

#t = Timer(5, getNewToken)
#t.start()


@app.route("/", methods = ['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/callback", methods = ['GET', 'POST'])
def listen():
    #r = requests.put('http://httpbin.org/put', data = {'key':'value'})
    myRequest = request.get_json()
    ACCESSCODE = myRequest['token']
    REFRESHCODE = myRequest['refresh']
    
    print(spotifyController.playSong(ACCESSCODE, 'Rick Astley', 'Never Gonna Give You Up'))

    return render_template('index.html')



@app.route("/sms")
def sms_reply():
    """Listen for SMS Messages and plays a song based the user's selection"""
    received_message = request.values.get('Body', None)
    incoming_command = received_message.split(DELIMITER)

    command = incoming_command[0]
    if (len(incoming_command) >= 3):
        artist = incoming_command[1]
        title = incoming_command[2]


    if (command.lower() == "play"):
        response_string = spotifyController.playSong(USERNAME, artist, title)
    elif (command.lower() == "vote"):
        response_string = spotifyController.vote(USERNAME, artist, title)
    elif (command.lower() == "list"):
        response_string = spotifyController.list_tracks(USERNAME)
    else:
        response_string = "Invalid Command %s" % command

    resp = MessagingResponse()
    msg = resp.message(response_string)

    return str(resp)



if __name__ == "__main__":
    app.run(host='localhost', debug=False)     #run debug


    #old sdk:3.7 (HelloData)
