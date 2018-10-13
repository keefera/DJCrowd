import spotipy
import os
import spotipy.util as util

def openCon():
	scope = "streaming app-remote-control user-modify-playback-state"
	token = util.prompt_for_user_token('akeefer6',scope,client_id='ffbf57e77cdc4d1f98b80bce63e16341',
		client_secret='1e612801fe654e4b956b07448461ee67',redirect_uri='http://localhost:8000')
	sp = spotipy.Spotify(token)
	artistName = "Rick Astley"
	trackName = "Never Gonna Give You Up"
	results = sp.search(q = 'artist:' + artistName + ' track:' + trackName, type = 'track')
	print(results)


if (__name__ == '__main__'):
	openCon()