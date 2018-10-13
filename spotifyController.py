import spotipy
import sys
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import json
import requests
import base64
import urllib
from flask import request

# consts
#Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
SPOTIFY_API_BASE_URL = "https://api.spotify.com"
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

CLIENT_ID = 'ffbf57e77cdc4d1f98b80bce63e16341'
CLIENT_SECRET = '1e612801fe654e4b956b07448461ee67'
CLIENT_SIDE_URL = "http://127.0.0.1"
PORT = 5000
REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
SCOPE = "streaming app-remote-control user-modify-playback-state user-read-playback-state"

def app_Authorization():
    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        # "state": STATE,
        # "show_dialog": SHOW_DIALOG_str,
        "client_id": CLIENT_ID
    }
    url_args = "&".join(["{}={}".format(key,urllib.parse.quote(val)) for key,val in auth_query_parameters.items()])
    auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
    return auth_url



def user_Authorization():
    auth_token = request.args['code']
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }
    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))
    headers = {"Authorization": "Basic {}".format(base64encoded)}
    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload, headers=headers)

    # Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Use the access token to access Spotify API
    authorization_header = {"Authorization":"Bearer {}".format(access_token)}
    return authorization_header


# Function plays song on spotify - limited to first result of query
# pass in spotify username, artist name, and track name
def playSong(username, artistName, trackName):
    #token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL)

    sp = spotipy.Spotify(auth=token)
    results = sp.search(q='artist:' + artistName + ' track:' + trackName, type='track', limit=1)

    try:
      trackURI = results['tracks']['items'][0]['uri']
    except:
      return "Error: No results found!"

    print(sp.current_user())

    devices = sp.devices()

    try:
      deviceID = devices['devices'][0]['id']
      sp.start_playback(device_id=deviceID, uris=[trackURI])
    except:
      return "Error: Spotify must be open on one of your devices!"

    return "Now playing: " + trackName + " by " + artistName

#TODO implement
def vote(username, artistName, trackName):
    global tracks
    tracks =[]
    tracks.append(title)
    return "voting for %s-%s" % (artistName, trackName)

def list_tracks (username):
    return "listing"

if (__name__ == '__main__'):
    if (len(sys.argv) != 4):
        print("Usage: spotifyController.py <username> <artistName> <trackName>")
        exit()

    print(playSong(sys.argv[1], sys.argv[2], sys.argv[3]))
