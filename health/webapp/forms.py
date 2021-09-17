from django import forms
from django.contrib.auth.models import User
from webapp import models
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
import datetime
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

class appointmentform(forms.ModelForm):

    class Meta:
        model=models.Appointment
        fields=('date','slot','description')

    def __init__(self,*args,**kwargs):
        super(appointmentform,self).__init__(*args,**kwargs)

        self.fields['slot'].queryset=models.Slot.objects.none()
        self.fields['slot'].widget.attrs['id']='slot'
        self.fields['date'].widget.attrs['id']='date'
        if 'date' in self.data:
            try:
                date = self.data.get('date')
                print("date")
                self.fields['slot'].queryset = models.Slot.objects.filter(date=date,start_time__gte=datetime.datetime.now()).order_by('start_time')
            except (ValueError, TypeError):
                print("OH NO!!")
