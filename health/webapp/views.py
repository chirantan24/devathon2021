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
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth.forms import PasswordResetForm
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
def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'barebears567@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"password_reset_form":password_reset_form})

def load_slots(request):
    date=request.GET.get('date')
    print(datetime.datetime.now())
    slots=models.Slot.objects.filter(date=date,start_time__gte=datetime.datetime.now()).order_by('start_time')
    return render(request,'student/dropdownlist.html',{'slots':slots})

class AppointmentCreate(LoginRequiredMixin,CreateView):
    login_url='login'
    model=models.Appointment
    form_class=forms.appointmentform
    template_name="student/addappointment.html"
    def get_success_url(self):
        return reverse_lazy('index')
    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.patient=models.Student.objects.get(user=self.request.user)
        self.object.doctor=models.Duty.objects.get(date=self.object.date).doc
        self.object.save()
        return super(AppointmentCreate,self).form_valid(form)

class AppointmentList(LoginRequiredMixin,ListView):
    login_url='login'
    model=models.Appointment
    template_name="appointments.html"
    context_object_name='appointments'
    def get_context_data(self,**kwargs):
        context=super(AppointmentList,self).get_context_data(**kwargs)
        age=[]
        for i in context['appointments']:
            age.append((int)(datetime.date.today().year - i.patient.birthdate.year + 1))
        context['appointments']=zip(context['appointments'],age)
        return context
    def get_queryset(self,*args,**kwargs):
        is_patient=models.Student.objects.all().filter(user=self.request.user).count()
        is_doctor=models.Doctor.objects.all().filter(user=self.request.user).count()
        if is_patient and not self.request.user.is_superuser:
            raise Http404
        elif is_doctor:
            return models.Appointment.objects.all().filter(doctor=models.Doctor.objects.get(user=self.request.user),date=datetime.date.today())
