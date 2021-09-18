from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class IntegerRangeField(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(IntegerRangeField, self).formfield(**defaults)
gender_choices={
("Female",'female'),
("Male",'male'),
("Transgender",'Transgender')
}
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    regno=IntegerRangeField(min_value=111111,max_value=999999,unique=True)
    contact=PhoneNumberField()
    birthdate=models.DateField(default="1980-01-01")
    gender=models.CharField(choices=gender_choices,default="Male",max_length=20)
    def __str__(self):
        return self.user.first_name

class Slot(models.Model):
    date=models.DateField()
    start_time=models.TimeField()
    end_time=models.TimeField()
    remaining=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.start_time.strftime("%H:%M") + "-" + self.end_time.strftime("%H:%M")

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    regno=models.CharField(max_length=50,unique=True)
    about=models.CharField(max_length=250,null=True)
    birthdate=models.DateField(default="1980-01-01")
    gender=models.CharField(choices=gender_choices,default="Male",max_length=20)
    def __str__(self):
        return "DR. " + self.user.first_name

class Duty(models.Model):
     date=models.DateField()
     doc=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True)
class Appointment(models.Model):
    patient =models.ForeignKey(Student,on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot,on_delete=models.CASCADE)
    description = models.CharField(max_length=300,null=True,blank=True)
    date=models.DateField()
    def __str__(self):
        return self.patient.__str__()+" - "+self.doctor.__str__()

class Receptionist(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    regno=models.CharField(max_length=50,unique=True)
    about=models.CharField(max_length=250,null=True)
    birthdate=models.DateField(default="1980-01-01")
    gender=models.CharField(choices=gender_choices,default="Male",max_length=20)
    def __str__(self):
        return "MR. " + self.user.first_name

blood_groups={
("A+",'A+'),
("A-","A-"),
("B+",'B+'),
("B-",'B-'),
("O+",'O+'),
("O-",'O-'),
("AB+",'AB+'),
("AB-",'AB-')
}
class Bio(models.Model):
    student=models.OneToOneField(Student,related_name='bio',on_delete=models.CASCADE,null=True)
    blood_group=models.CharField(choices=blood_groups,default="A+",max_length=4)
    PWD=models.BooleanField()
    Remarks=models.CharField(max_length=250)
    weight=models.PositiveIntegerField()
    Address=models.CharField(max_length=250)
    profile_pic=models.ImageField(upload_to='profile_pics/',blank=True,null=True)

class Record(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    title=models.CharField(max_length=100)
    date=models.DateField()
    file1=models.FileField(upload_to='files',null=True,blank=True)
    file2=models.FileField(upload_to='files',null=True,blank=True)
    details=models.CharField(max_length=500,null=True,blank=True)
