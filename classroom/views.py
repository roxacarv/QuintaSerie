from django.shortcuts import render
import pyrebase

# Create your views here.

config = {
    "apiKey": "AIzaSyAerk1eqSvs9GACOrCgQHcVGu1iJgUJz54",
    "authDomain": "a-quinta-serie.firebaseapp.com",
    "projectId": "a-quinta-serie",
    "storageBucket": "a-quinta-serie.appspot.com",
    "messagingSenderId": "24322454020",
    "appId": "1:24322454020:web:14333c0e56fa9f31f23b51",
    "measurementId": "G-RNM2R6QF9J",
    "databaseURL": "https://a-quinta-serie-default-rtdb.firebaseio.com"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()

def index(requests):
    app_name = database.child('Data').child('ProjectName').get().val()
    print(app_name)
    return render(requests, 'index.html', {'app_name': app_name})