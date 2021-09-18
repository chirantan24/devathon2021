from django.urls import path
from . import views
app_name='app'
urlpatterns=[
path('request/',views.AppointmentCreate.as_view(),name='request'),
path('appointments/',views.get_appointments,name='appointments'),
path('record/<pk>/',views.record,name='record'),
path('records',views.get_records,name='records'),
path('createbio/',views.Create_bio.as_view(),name='createbio'),
path('updatebio/<pk>',views.update_bio.as_view(),name='updatebio'),
path('appointment/delete/<pk>',views.AppointmentDelete.as_view(),name='appointmentdelete'),
path('appointment/update/<pk>',views.AppointmentUpdate.as_view(),name='appointmentupdate'),
path('appointments/<pk>/',views.AppointmentDetail.as_view(),name='appointmentdetail'),
]
