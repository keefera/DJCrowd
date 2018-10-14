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


SONGS = {}
sorted_songs = []

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

    deviceID = devices['devices'][0]['id']
    sp.start_playback(device_id=deviceID, uris=[trackURI])

    #except:
    #return "Error: Spotify must be open on one of your devices!"

    return "Now playing: " + artistName + " : " + trackName

'''
def checkPlayback(token):
    global SONGS
    if SONGS:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_playback
        progress = results['progress_ms']
        total = results['duration_ms']
        print(total - progress)
        if total - progress <= 10000:
            playNext(token)
'''

def playNext(token):
    top_key = getNextSong()
    popKeyValue(top_key)
    artist_title_pair = top_key.split("::")
    artist = artist_title_pair[0]
    title = artist_title_pair[1]
    playSong(token, artist, title)

def getNextSong():
    global sorted_songs
    sorted_songs = sortDictionaryByValue
    return next(iter(sorted_songs))[0]

def popKeyValue(key):
    global SONGS
    del SONGS[key]

def vote(artistName, trackName):
    global SONGS
    key = "%s::%s" % (artistName.lower().strip(), trackName.lower().strip())
    dictionary_index = indexDictionary(key)
    if (dictionary_index):
        votes = SONGS[key]
        SONGS[key] = votes + 1
    else:
        votes = 1
        SONGS.update ({key : votes})
    return "Voting for %s : %s" % (artistName, trackName)

def indexDictionary(key):
    global SONGS
    if(key in SONGS):
        return True
    return False

def sortDictionaryByValue():
    global SONGS
    return sorted(SONGS.items(), key = lambda kv: kv[1])

def list_tracks():
    global SONGS

    for i in SONGS:
        pair = i.split("::")
        out = "%s - %s\n votes: %s" % (pair[0], pair[1], SONGS[i])

    return str(out)

if (__name__ == '__main__'):
    print('')
    #print(playSong(sys.argv[1], sys.argv[2], sys.argv[3]))
    #print(playSong(MYTOKEN, 'Arctic Monkeys', 'Cornerstone'))
