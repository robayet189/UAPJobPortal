from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('register/studentregistration/', views.studentregistration, name='stdreg'),
    path('register/alumniregistration/', views.alumniregistration, name='almreg'),
    path('register/facultyregistration/', views.facultyregistration, name='fcltreg'),
    path('register/companyregistration/', views.companyregistration, name='comreg'),
    path('register/adminregistration/', views.adminregistration, name='adminreg'),
    path('login/studentlogin/', views.studentlogin, name='stdlog'),
    path('login/alumnilogin/', views.alumnilogin, name='almlog'),
    path('login/facultylogin/', views.facultylogin, name='fcltlog'),
    path('login/companylogin/', views.companylogin, name='comlog'),
    path('login/adminlogin/', views.adminlogin, name='adminlog'),
    path("success/", views.success, name="success"),
]