from django.contrib import messages
from .models import Patient, Doctor, Hospital,MedicalRecords
from email.header import Header
from django.conf import settings
from django.utils import timezone
import json
import os
from datetime import datetime
import random
from django.db.models import Q
import string
from django.core.mail import EmailMessage
from django.template import loader
import hashlib
import time
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText



def ReceivePatient(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        gender = data.get('gender')
        age = data.get('age')
        idCard = data.get('idCard')
        phone_number = data.get('phone_number')
        address = data.get('address')
        adminpassword = data.get('adminpassword')
        if(adminpassword =="Bravo"):
            if Patient.objects.filter(phone_number=phone_number).exists():
                response = JsonResponse({'message': "phone is already existing",
                                         "success": 0
                                         }, status=200)
                return response
            else:
                patient = Patient(
                    username=username,
                    phone_number=phone_number,
                    gender=gender,
                    age=age,
                    idCard=idCard,
                    address=address,
                    password=password
                )
                # 保存新的Patient对象
                patient.save()
                response = JsonResponse({'message': "mession is done",
                                         "success": 0
                                         }, status=200)
                return response
        else:
            response = JsonResponse({'message': "method not allowed",
                                     "success": 0
                                     }, status=200)
            return response
    else:
        response = JsonResponse({'message': "method not allowed",
                                 "success": 0
                                 }, status=200)
        return response

