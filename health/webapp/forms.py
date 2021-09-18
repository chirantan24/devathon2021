from django import forms
from django.contrib.auth.models import User
from webapp import models
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.forms.widgets import SelectDateWidget
import datetime
from phonenumber_field.widgets import PhoneNumberPrefixWidget
class DateInput(forms.DateInput):
    input_type = 'date'

class userform(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
    class Meta():
        model=User
        fields=('email','first_name','last_name','password1','password2')

class studentform(forms.ModelForm):

    class Meta:
        model=models.Student
        fields=('regno','birthdate','contact')
        widgets={
            'birthdate':DateInput(),
            'contact':PhoneNumberPrefixWidget(initial='NL'),
        }
class appointmentform(forms.ModelForm):

    class Meta:
        model=models.Appointment
        fields=('date','slot','description')
        widgets={
            'date':DateInput()
        }
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
class BioForm(forms.ModelForm):
    class Meta:
        model=models.Bio
        fields=('blood_group','weight','PWD','Address','Remarks','profile_pic')
        widgets={
        'Address': forms.Textarea(attrs={"cols":40,"rows":5,"placeholder":'Enter your Address here.'}),
        'Remarks': forms.Textarea(attrs={"cols":40,"rows":5,"placeholder":'Enter your Remarks here.(e.g. birthmark)'}),
        }

        labels={
        'blood_group':'Blood Group',
        'profile_pic':'Upload Profile pic'
        }

class RecordForm(forms.ModelForm):
    weight = forms.IntegerField()
    class Meta:
        model=models.Record
        fields = ('title','date','weight','file2','details')
        widgets={
        'details':forms.Textarea(attrs={"cols":40,"rows":5,"placeholder":'Enter Details here.'}),
        }
    def __init__(self,*args,**kwargs):
        super(RecordForm,self).__init__(*args,**kwargs)
        self.fields['title'].widget.attrs['readonly']=True
        self.fields['date'].widget.attrs['readonly']=True
