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
CLIENT_SIDE_URL = "http://localhost"
PORT = 5000
REDIRECT_URI = "{}:{}/callback".format(CLIENT_SIDE_URL, PORT)
SCOPE = "streaming app-remote-control user-modify-playback-state user-read-playback-state user-read-currently-playing user-follow-read user-follow-modify user-read-email user-read-private user-read-birthdate user-library-read"

MYTOKEN = 'BQAeHoSCLjGYUzodzBkGxL5bMyWwflmdHhZ2Xn36GMNAvFDTK5L02J1pePWq7TN-AioaGRXBWnZN4cB4g6Znq4QNK-TG6R1hm9Fdw5K043zXLNAuHVXo7ChJdqJyMtYehurcwxNYL_zH2eEFbT7Eocu81gEnBpr82Bi02lBtnJG8'

'''
URL = "https://accounts.spotify.com/en/authorize?client_id=ffbf57e77cdc4d1f98b80bce63e16341&response_type=code&redirect_uri=http:%2F%2Flocalhost:5000%2Fcallback&scope=streaming%20app-remote-control%20user-modify-playback-state%20user-read-playback-state&state=34fFs29kd09"
sp_oauth = spotipy.oauth2.SpotifyOAuth( CLIENT_ID, CLIENT_SECRET,REDIRECT_URI,scope=SCOPE)
url = "http://localhost:5000/callback?code=AQAUg4bEUQFMayxdxZrFFx8iBRqc4gfoL-b2WVZO5NHLZuG4L1CX7YeQ-pCCcemeJcL94isrL6-em_k2GcKql1dZnKX11ESCs-qzFOIP3zC35Ypim10p5KA2S4tueRay6LryPrtAa6wCd-JPbkJ167E9hbqqBN8KcjoiSxBTfSzm9bBlLx5-PttQbJUtX50-D7pOYbk9RGloGMKQfD9YPhU84hJHt_GEQ6MNwSKB_SJ2HtPTyQ-PH7u3nmO9ALgPPqkCw6VD3sZSfzFivDzQEDwQqm5ig5pv1-eErBWn_Q0raqbZj-V-uyWUHQ&state=34fFs29kd09"
code = sp_oauth.parse_response_code(url)
token_info = sp_oauth.get_access_token(code)
access_token = token_info['access_token']
'''


# Function plays song on spotify - limited to first result of query
# pass in spotify username, artist name, and track name
def playSong(token, artistName, trackName):
    #token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, REDIRECT_URL)

    sp = spotipy.Spotify(auth=token)
    results = sp.search(q='artist:' + artistName + ' track:' + trackName, type='track', limit=1)

    try:
      trackURI = results['tracks']['items'][0]['uri']
    except:
      return "Error: No results found!"

    devices = sp.devices()
    print(devices)

    
    deviceID = devices['devices'][0]['id']
    sp.start_playback(device_id=deviceID, uris=[trackURI])

    #except:
    #return "Error: Spotify must be open on one of your devices!"

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

    #print(playSong(sys.argv[1], sys.argv[2], sys.argv[3]))
    print(playSong(MYTOKEN, 'Arctic Monkeys', 'Cornerstone'))
