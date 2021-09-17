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
class Student(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    regno=IntegerRangeField(min_value=111111,max_value=999999,unique=True)
    contact=PhoneNumberField()
    def __str__(self):
        return self.user.first_name
