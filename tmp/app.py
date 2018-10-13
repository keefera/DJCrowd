from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming calls with a MMS message."""
    # Start our TwiML response
    body = "\"" + request.values.get('Body', None) + "\""

    resp = MessagingResponse()

    # Add a text message
    msg = resp.message("Selecting Song %s" % body)


    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
