from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

import spotifyController

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a MMS message."""
    # Start our TwiML response
    body = request.values.get('Body', None)

    song = body.split("%%")

    artist = song[0]
    title = song[1]

    spotifyController.playSong("akeefer6",artist,title)

    resp = MessagingResponse()

    # Add a text message
    msg = resp.message("Selecting Song \"%s\", \"%s\"" % (artist,title))


    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
