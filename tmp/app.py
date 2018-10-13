from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

import spotifyController

DELIMITER = "%%"
USERNAME = "agentquebeq"

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def sms_reply():
    """Listen for SMS Messages and plays a song based the user's selection"""
    received_message = request.values.get('Body', None)

    artist_song_pair = received_message.split(DELIMITER)

    artist = artist_song_pair[0]
    title = artist_song_pair[1]

    spotifyController.playSong(USERNAME, artist, title)

    resp = MessagingResponse()
    msg = resp.message("Playing Song: \"%s\", \"%s\"." % (artist,title))

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)     #run debug


    #old sdk:3.7 (HelloData)
