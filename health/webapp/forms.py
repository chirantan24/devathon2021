from django import forms
from django.contrib.auth.models import User
from webapp import models
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone

class userform(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta():
        model=User
        fields=('email','first_name','last_name','password1','password2')

class studentform(forms.ModelForm):

    class Meta:
        model=models.Student
        fields=('regno','contact')
