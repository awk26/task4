from django import forms
from .models import *


class LoginForm(forms.Form):
    uname=forms.CharField(max_length=30,label="username")
    pswd=forms.CharField(max_length=30,label="password")




class FileUploadForm(forms.Form):
    files = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))




