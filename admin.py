import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials
from firebase_admin import auth

cred = credentials.Certificate(
    "rainbow/visspot-3cf67-firebase-adminsdk-z19vl-0c10395aae.json")
firebase_admin.initialize_app(
    cred, {'databaseURL': 'https://visspot-3cf67.firebaseio.com', 'authDomain': 'visspot-3cf67.firebaseapp.com'})

db = firestore.client()
story_ref = db.collection(u'stories')
dataset_ref = db.collection(u'datasets')
chart_ref = db.collection(u'charts')
apikey_ref = db.collection(u'apiKeys')
