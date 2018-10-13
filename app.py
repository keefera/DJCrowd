from flask import Flask, request, redirect, render_template
from twilio.twiml.messaging_response import MessagingResponse

import spotifyController

DELIMITER = "::"
USERNAME = "akeefer6"

app = Flask(__name__)


@app.route("/")
def index():
    auth_url = spotifyController.app_Authorization()
    return redirect(auth_url)


@app.route("/callback")
def listen():
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
    app.run(host='localhost', debug=True)     #run debug


    #old sdk:3.7 (HelloData)
