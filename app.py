from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import MessagingResponse
from threading import Timer
from multiprocessing import Process, Value
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

@app.route("/playSong", methods = ['GET', 'POST'])
def playVoted():
    global ACCESSCODE
    if ACCESSCODE != "":
        spotifyController.playNext(ACCESSCODE)

    return render_template('index.html', tabel_data = spotifyController.getSongs())

@app.route("/callback", methods = ['GET', 'POST'])
def listen():
    #r = requests.put('http://httpbin.org/put', data = {'key':'value'})
    myRequest = request.get_json()
    global ACCESSCODE
    global REFRESHCODE
    ACCESSCODE = myRequest['token']
    REFRESHCODE = myRequest['refresh']
    spotifyController.check(ACCESSCODE)
    
    #print(spotifyController.playSong(ACCESSCODE, 'Rick Astley', 'Never Gonna Give You Up'))

    return render_template('index.html', tabel_data = spotifyController.getSongs())


@app.route("/sms", methods = ['GET', 'POST'])
def sms_reply():
    """Listen for SMS Messages and plays a song based the user's selection"""
    received_message = request.values.get('Body', None)
    incoming_command = received_message.split(DELIMITER)

    command = incoming_command[0]
    artist = ""
    title = ""
    if (len(incoming_command) >= 3):
        artist = incoming_command[1]
        title = incoming_command[2]


    if (command.lower() == "play"):
        response_string = spotifyController.playSong(ACCESSCODE, artist, title)
    elif (command.lower() == "vote"):
        response_string = spotifyController.vote(artist, title)
    elif (command.lower() == "list"):
        response_string = spotifyController.list_tracks()
    else:
        response_string = "Invalid Command %s" % command

    resp = MessagingResponse()
    msg = resp.message(response_string)

    return str(resp)


def voteLoop():
    while(True):
        global ACCESSCODE
        if ACCESSCODE != "":
            spotifyController.checkPlayback(ACCESSCODE)


if __name__ == "__main__":
    #recording_on = Value('b', True)
    p = Process(target=voteLoop)
    p.start()  
    app.run(debug=False, use_reloader=False)
    p.join()


    #old sdk:3.7 (HelloData)
