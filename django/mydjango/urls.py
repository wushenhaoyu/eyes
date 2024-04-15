"""
URL configuration for mydjango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from user.views import gender,test,getUserList,PatientAdvice,getHistoryUserList,index_vue,geturl,getALLUserList
from django.contrib import admin
from user.DoctorView import post_email,doctor_login,register_doctor
from user.WXReceive import ReceivePatient,save_media,update_patinet_message,change_hospital
from user.Hospital import hospital,GenerateHospitalAuthCode,getALLhosoitallist
urlpatterns = [
    path('', index_vue),
    path('index/', index_vue),
    path('api/index/', index_vue),
    path('register/',register_doctor),
    path('api/register/',register_doctor),
    path("login/",doctor_login),
    path("api/login/",doctor_login),
    path("email/",post_email),
    path("api/email/",post_email),
    path("user/gender",gender),
    path("api/user/gender",gender),
    path("test",test),
    path("api/test",test),
    path("Bravo/hospital/eye/register",GenerateHospitalAuthCode),
    path("api/Bravo/hospital/eye/register",GenerateHospitalAuthCode),
    path("getpatientwaittinglist/",getUserList),
    path("api/getpatientwaittinglist/",getUserList),
    path("getpatienthistorylist/",getHistoryUserList),
    path("api/getpatienthistorylist/",getHistoryUserList),
    path("ReceivePatient/",ReceivePatient),
    path("api/ReceivePatient/",ReceivePatient),

    path("UpdatePatientMessage/",update_patinet_message),
    path("api/UpdatePatientMessage/",update_patinet_message),

    path("getpatientalllist/",getALLUserList),
    path("api/getpatientalllist/",getALLUserList),

    path("changeHospital/",change_hospital),
    path("api/changeHospital/",change_hospital),


    path("geturl/",geturl),
    path("api/geturl/",geturl),

    path("getALLhosoitallist/",getALLhosoitallist),
    path("api/getALLhosoitallist/",getALLhosoitallist),

    path("ReceiveMedia/",save_media),
    path("api/ReceiveMedia/",save_media),
    path("getUserList/",getUserList),
    path("api/getUserList/",getUserList),
    path("hospital",hospital),
    path("api/hospital",hospital),
    path('admin/', admin.site.urls),
    path('patientadvice/', PatientAdvice),
    path('api/patientadvice/', PatientAdvice),

]