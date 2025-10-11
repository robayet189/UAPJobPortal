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
    path('browseoppurtunity/', views.browse_opportunities, name='browse_opportunities'),
    path('api/search_jobs/', views.search_jobs, name='search_jobs'),
    path('browseoppurtunity/job_id/', views.job_id, name='job_id'),
<<<<<<< HEAD

    path('forgotpassword/<str:source>/', views.forgotpassword, name='forgotpass'),
    path('sendrecoverycode/<str:source>/', views.sendrecoverycode, name='sendrecoverycode'),
    path('tryanotheremail/<str:source>/', views.tryanotheremail, name='tryanotheremail'),
    path('sendcodenewmail/<str:source>/', views.sendcodenewmail, name='sendcodenewmail'),
    path('resetpassword/<str:source>/', views.resetpassword, name='resetpassword'),
    path('resetpasswordsuccess/<str:source>/', views.resetpasswordsuccess, name='resetpasswordsuccess'),
    path('verify-code/<str:source>/', views.verify_code, name='verify_code'),

]
=======
    path('dashboard/', views.dashboard, name='dashboard'),
]
>>>>>>> 7d380c34a20211d592a2c4a254a06c38875c1d9d
