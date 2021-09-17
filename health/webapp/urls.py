from django.urls import path
from . import views
app_name='app'
urlpatterns=[
path('request/',views.AppointmentCreate.as_view(),name='request'),
]
