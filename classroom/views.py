from datetime import date
from django.http import HttpResponseRedirect
import pyrebase
from django.shortcuts import redirect, render
from . import credentials as conf
from .User import User
from .forms import NameForm
import random
import string

# Create your views here.

firebase = pyrebase.initialize_app(conf.config)
authe = firebase.auth()
database = firebase.database()

# Teste de inserção de usuário no BD usando o objeto User
'''rodrigo = User()
rodrigo.first_name = "Rodrigo"
rodrigo.email = "xavier@gmail.com"
rodrigo.password = "123456"
rodrigo.insert_update_to_database()'''

# Fazendo query de usuários
'''user1 = User.find_by_email("xavier@gmail.com")
user2 = User.find_by_first_name("Carlos")
user3 = User.find_by_id(3)'''

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


def create_class(request):
    if request.method == 'POST':
        letters = string.ascii_uppercase
        classcode = ''.join(random.choice(letters) for i in range(6))
        classadmin = request.POST.get('classadmin')
        classname = request.POST.get('classname')
        discipline = request.POST.get('discipline')
        database.child('Classroom').set(
            {
                'classadmin' : classadmin,
                'classname' : classname,
                'discipline' : discipline,
                'classcode': classcode,
            }
        )
        classadm =  database.child('Classroom').child('classadmin').get().val()
        classname = database.child('Classroom').child('classname').get().val()
        classcode = database.child('Classroom').child('classcode').get().val()
        return render(request, 'join.html', {
        'classadm': classadm,
        'classname': classname,
        'classcode': classcode,
        })
    return render(request, 'create.html')


def join_class(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        post = request.GET.get('post')
        time = date.today()
        post_time = time.strftime("%H:%M %d/%m/%Y")
        database.child('Classroom').child('post').set(
            {'name': name, 'post': post, 'post_time': post_time }
        )
        redirect('join.html')
    classadm =  database.child('Classroom').child('classadmin').get().val()
    classname = database.child('Classroom').child('classname').get().val()
    classcode = database.child('Classroom').child('classcode').get().val()
    
    return render(request, 'join.html', {
        'name': name,
        'classadm': classadm,
        'classname': classname,
        'post': post,
        'post_time': post_time,
        'classcode': classcode,
        })