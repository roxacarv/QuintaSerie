from django.http import HttpResponseRedirect
import pyrebase
from django.shortcuts import render
from . import credentials as conf
from .forms import NameForm

# Create your views here.

firebase = pyrebase.initialize_app(conf.config)
authe = firebase.auth()
database = firebase.database()

database.child("users").update({"name": "Xavier", "pass": "1234567"})

def index(request):
    app_name = database.child('Data').child('ProjectName').get().val()
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            udata = {"user": form.cleaned_data["uname"], "pass": form.cleaned_data["upass"]}
            database.child("users").push(udata)
    else:
        form = NameForm()
    return render(request, 'index.html', {'app_name': app_name, 'form': form})