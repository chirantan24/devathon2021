"""health URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from webapp import views
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('',views.index,name='index'),
    path('admin/', admin.site.urls),
    path('register/',views.register,name='register'),
    path('login/',auth_view.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout/',auth_view.LogoutView.as_view(),name='logout'),
    path('load_slots/',views.load_slots,name='load_slots'),
    path('password_reset/',views.password_reset_request,name='password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(template_name='password/password_reset_complete.html'), name='password_reset_complete'),
    path('app/',include('webapp.urls')),
]
