from django import forms

class NameForm(forms.Form):
    uname = forms.CharField(label='Usuário', max_length=100)
    upass = forms.CharField(label='Senha', max_length=100)