import spotipy
import sys
import spotipy.util as util
import pyrebase

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


#Initialize Firebase with service account credentials
def initdb():
	config = {
  	"apiKey": "AIzaSyAjFT-Kc-sYP8BQw7787SD9fcc5kbPOYOQ",
  	"authDomain": "dj-crowd.firebaseapp.com",
  	"databaseURL": "https://dj-crowd.firebaseio.com",
  	"storageBucket": "dj-crowd.appspot.com",
  	"serviceAccount": "service_account_cred.json"
	}
	firebase = pyrebase.initialize_app(config)
	return firebase.database()

def pulldb(db):
    vote_info = db.child("Votes").get()
    votes = [i.val() for i in vote_info.each()][0]
    return votes

def pushdb(db, votes):
	db.child("Votes").push(votes)

def cleardb(db):
	db.remove()


if (__name__ == '__main__'):
	if (len(sys.argv) != 4):
		print("Usage: spotifyController.py <username> <artistName> <trackName>")
		exit()

	db = initdb()

	playSong(sys.argv[1], sys.argv[2], sys.argv[3])
