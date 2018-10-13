import spotipy
import sys
import spotipy.util as util

#Function plays song on spotify - limited to first result of query
#pass in spotify username, artist name, and track name
def playSong(username, artistName, trackName):
	scope = "streaming app-remote-control user-modify-playback-state user-read-playback-state"
	token = util.prompt_for_user_token(username, scope, client_id='ffbf57e77cdc4d1f98b80bce63e16341',
		client_secret='1e612801fe654e4b956b07448461ee67', redirect_uri='http://localhost:8000')
	sp = spotipy.Spotify(auth = token)
	results = sp.search(q = 'artist:' + artistName + ' track:' + trackName, type = 'track', limit = 1)
	if not results['tracks']['items']:
		print("Error: No results found")
		exit()
		
	trackURI = results['tracks']['items'][0]['uri']
	devices = sp.devices()
	if not devices['devices']:
		print("Error: Spotify must be open on one of your devices!")
		exit()
	
	deviceID = devices['devices'][0]['id']
	sp.start_playback(device_id = deviceID, uris = [trackURI])

	#start_playback(device_id=None, context_uri=None, uris=None)


if (__name__ == '__main__'):
	if (len(sys.argv) != 4):
		print("Usage: spotifyController.py <username> <artistName> <trackName>")
		exit()

	playSong(sys.argv[1], sys.argv[2], sys.argv[3])