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
from django.contrib.auth.decorators import login_required
from fpdf import FPDF
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
        subject="Appointment Scheduled on {}".format(self.object.date)
        email="Hey {},\n Your Appointment to despensary NITW is scheduled on {}".format(self.request.user.first_name,self.object.date)
        send_mail(subject,email,'barebears567@gmail.com',[self.request.user.email],fail_silently=False)
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

class AppointmentDelete(LoginRequiredMixin,DeleteView):
    login_url='login'
    model=models.Appointment
    template_name='appointment_confirm_delete.html'
    def get_context_data(self,**kwargs):
        context=super(AppointmentDelete,self).get_context_data(**kwargs)
        is_rec=models.Receptionist.objects.all().filter(user=self.request.user).count()
        if  self.request.user.is_superuser or is_rec or context['object'].patient==self.request.user.student:
            return context
        else:
            raise Http404
    def get_success_url(self):
        subject="Appointment Cancelled on {}".format(self.object.date)
        email="Hey {},\n Your Appointment to despensary NITW scheduled on {} is Cancelled".format(self.object.patient.user.first_name,self.object.date)
        send_mail(subject,email,'barebears567@gmail.com',[self.object.patient.user.email],fail_silently=False)
        return reverse_lazy('index')
class AppointmentDetail(LoginRequiredMixin,DetailView):
    login_url='login'
    model=models.Appointment
    template_name="receptionist/appointment_detail.html"
    def get_context_data(self,**kwargs):
        context=super(AppointmentDetail,self).get_context_data(**kwargs)
        is_rec=models.Receptionist.objects.all().filter(user=self.request.user).count()
        context['is_rec']=is_rec or self.request.user.is_superuser
        if  self.request.user.is_superuser or is_reccontext['object'].patient==self.request.user.student :
            return context
        else:
            raise Http404

class AppointmentUpdate(LoginRequiredMixin,UpdateView):
    login_url='login'
    model=models.Appointment
    form_class=forms.appointmentform
    template_name="student/addappointment.html"
    def get_context_data(self,**kwargs):
        context=super(AppointmentUpdate,self).get_context_data(**kwargs)
        is_rec=models.Receptionist.objects.all().filter(user=self.request.user).count()
        if  self.request.user.is_superuser or is_rec or context['object'].patient==self.request.user.student:
            return context
        else:
            raise Http404
    def get_success_url(self):
        return reverse_lazy('index')
    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.patient=models.Student.objects.get(user=self.request.user)
        self.object.doctor=models.Duty.objects.get(date=self.object.date).doc
        self.object.save()
        subject="Appointment Scheduled on {}".format(self.object.date)
        email="Hey {},\n Your Appointment to despensary NITW is updated and scheduled on {}".format(self.object.patient.user.first_name,self.object.date)
        send_mail(subject,email,'barebears567@gmail.com',[self.object.patient.user.email],fail_silently=False)
        return super(AppointmentCreate,self).form_valid(form)

def record(request,pk):
    is_rec=models.Receptionist.objects.all().filter(user=request.user).count()
    if not is_rec and not request.user.is_superuser:
        raise Http404
    appointment=models.Appointment.objects.get(id=pk)
    if request.method == "POST":
        form=forms.RecordForm(request.POST,request.FILES)
        obj=form.save(commit=False)
        pdf=FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=24)
        pdf.cell(200,10,txt="Appointment {}".format(pk),ln=1,align='C')
        name="{}".format(pk)
        pdf.set_font("Arial", size=16)
        pdf.cell(200,10,txt="Reg No : {}".format(appointment.patient.regno),ln=1)
        pdf.cell(200,10,txt="Name : {} {}".format(appointment.patient.user.first_name,appointment.patient.user.last_name),ln=1)
        pdf.cell(200,10,txt="Date : {}".format(appointment.date),ln=1)
        pdf.cell(200,10,txt="Time : {}".format(datetime.datetime.now().time()),ln=1)
        pdf.cell(200,10,txt="Doctor : {}".format(appointment.doctor),ln=1)
        pdf.cell(200,10,txt="Weight : {}".format(request.POST['weight']),ln=1)
        pdf.cell(200,10,txt="Description: {}".format(appointment.description),ln=1)
        pdf.cell(200,10,txt="Doctor's Remarks : {}".format(obj.details),ln=1)
        pdf.cell(200,10,txt="Receptionist",ln=1,align='R')
        pdf.cell(200,10,txt="{}".format(request.user.first_name),ln=1,align='R')
        # file1=
        # create file1
        rec=models.Record(title=obj.title,student=appointment.patient,file2=obj.file2,details=obj.details,date=obj.date)
        pdf.output("media/files/"+name+".pdf",dest='F')
        rec.file1.name="files/"+name+".pdf"
        rec.save()
        # appointment.delete()
        return HttpResponseRedirect(reverse_lazy('app:appointments'))
    else :
        temp=models.Record(title="Appointment {}".format(appointment.id),student=appointment.patient,date=datetime.date.today())
        form=forms.RecordForm(instance=temp)
    return render(request,'receptionist/addrecord.html',context={"form":form})


class Create_bio(LoginRequiredMixin,CreateView):
    model=models.Bio
    login_url='login'
    template_name='student/bio_create.html'
    success_url=reverse_lazy('index')
    form_class=forms.BioForm
    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        return super(Create_bio,self).form_valid(form)
class update_bio(LoginRequiredMixin,UpdateView):
    model=models.Bio
    login_url='login'
    template_name='student/bio_create.html'
    success_url=reverse_lazy('index')
    form_class=forms.BioForm
    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user;
        self.object.save()
        return super(update_bio,self).form_valid(form)
    def get_context_data(self,**kwargs):
        context=super(update_bio,self).get_context_data(**kwargs)
        if context['object'].student==self.request.user.student or self.request.user.is_superuser:
            return context
        else:
            raise Http404
def load_appointments_rec(request):
    date=request.GET.get('date')
    appointments=models.Appointment.objects.all().filter(date=date).order_by('slot')
    age=[]
    for i in appointments:
        age.append((int)(datetime.date.today().year - i.patient.birthdate.year + 1))
    appointments=zip(appointments,age)
    return render(request,'student/table_rows.html',{'appointments':appointments})

def load_appointments_doc(request):
    date=request.GET.get('date')
    duty=models.Duty.objects.all().filter(date=date,doc=request.user.doctor).count()
    appointments=models.Appointment.objects.all().filter(date=date,doc=request.user.doctor).order_by('slot')
    age=[]
    for i in appointments:
        age.append((int)(datetime.date.today().year - i.patient.birthdate.year + 1))
    appointments=zip(appointments,age)
    return render(request,'student/table_rows.html',{'appointments':appointments,'duty':duty})

def load_appointments_student(request):
    date=request.GET.get('date')
    print(date)
    appointments=models.Appointment.objects.all().filter(date=date,patient=request.user.student)
    age=[]
    for i in appointments:
        print("hello")
        age.append((int)(datetime.date.today().year - i.patient.birthdate.year + 1))
    appointments=zip(appointments,age)
    return render(request,'student/table_rows.html',{'appointments':appointments})
@login_required
def get_appointments(request):
    is_rec=models.Receptionist.objects.all().filter(user=request.user).count()
    is_doctor=models.Doctor.objects.all().filter(user=request.user).count()
    is_superuser=request.user.is_superuser
    if is_rec or is_superuser:
        return render(request,'appointments.html',{'role':'R'})
    elif is_doctor:
        return render(request,'appointments.html',{'role':'D'})
    else :
        return render(request,'appointments.html',{'role':'S'})

@login_required
def get_records(request):
    is_rec=models.Receptionist.objects.all().filter(user=request.user).count()
    is_doctor=models.Doctor.objects.all().filter(user=request.user).count()
    is_superuser=request.user.is_superuser
    if is_rec or is_superuser or is_doctor:
        records=models.Record.objects.all().order_by('-date')
        return render(request,'records.html',{'records':records})
    else :
        records=models.Record.objects.filter(student=request.user.student).order_by('-date')
        return render(request,'records.html',{'records':records})
# TODO: Medicines inventory,staff notif , make pdf from data to upload, testing file uploads, front end
