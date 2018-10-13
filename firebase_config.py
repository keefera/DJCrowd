import pyrebase

#Initialize Firebase with service account credentials
config = {
  "apiKey": "AIzaSyAjFT-Kc-sYP8BQw7787SD9fcc5kbPOYOQ",
  "authDomain": "dj-crowd.firebaseapp.com",
  "databaseURL": "https://dj-crowd.firebaseio.com",
  "storageBucket": "dj-crowd.appspot.com",
  "serviceAccount": "service_account_cred.json"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

#retrieve vote data
def get_votes():
    vote_info = db.child("Votes").get()
    votes = [i.val() for i in vote_info.each()][0]
    return votes

#clears out all data
def clear_data():
    db.remove()

votes = {"song1": 5, "song2": 7, "song3": 4}

#upload votes
def upload_votes(votes):
    db.child("Votes").push(votes)



