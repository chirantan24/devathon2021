from django.shortcuts import render
from webapp import forms
from django.urls import reverse,reverse_lazy
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, JsonResponse,Http404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.views.generic import TemplateView,CreateView,DeleteView,ListView,DetailView,UpdateView
from webapp import models
import datetime,time
from django.utils import timezone
# Create your views here.
def index(request) :
  return render(request,'index.html')

def register(request):
    if request.method == 'POST':
        form1=forms.userform(data=request.POST)
        form2=forms.studentform(data=request.POST)
        if form1.is_valid() and form2.is_valid():
            user = form1.save()
            student = form2.save(commit=False)
            user.username=student.regno
            user.save()
            student.user=user
            student.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form1=forms.userform()
        form2=forms.studentform()
    return render(request,'register.html',context={'form1':form1,'form2':form2})
