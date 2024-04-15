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


##审核医院注册
def hospital(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        location = request.POST['location']
        photo= request.FILES.get('file')
        print(name, email, location, photo)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        save_folder = os.path.join(parent_dir, 'HospitalAccreditationDocuments')
        index = 1
        # 检查目标文件夹是否存在，如果不存在则创建
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        filename =name+email
        while os.path.exists(os.path.join(save_folder, filename)):
            filename = f"{name}({index})"
            index +=1

        photoname = filename+".png"
        save_path = os.path.join(save_folder, photoname)
        print(save_path)
        with open(save_path, 'wb') as f:
            for chunk in photo.chunks():
                f.write(chunk)
        textname = filename+".txt"
        text_path = os.path.join(save_folder, textname)
        with open(text_path, 'w') as text_file:
            text_file.write(f"Name: {name}\nEmail: {email}\nLocation: {location}")
        response = JsonResponse({'message': "success",
                                 "success": 0
                                 }, status=200)
        return response



##生成验证码函数
def generate_verification_code(length=5):
    # 生成包含数字和大写字母的随机验证码
    characters = string.digits + string.ascii_uppercase
    verification_code = ''.join(random.choices(characters, k=length))
    return verification_code



##成成医院的验证码
def GenerateHospitalAuthCode(request):
    if request.method == "POST":
        data = json.loads(request.body)
        B = data.get("B")
        if B!="Bravo":
            response = JsonResponse({'message': "warning:please go ",
                                     "success": 0
                                     }, status=404)
            return response
        name = data.get("name")
        code = generate_verification_code(8)
        while Hospital.objects.filter(hospital_auth_code=code).exists():
            code = generate_verification_code()
        province = data.get("province")
        city = data.get("city")
        if name and province and city:
            if Hospital.objects.filter(name=name).exists():
                response = JsonResponse({'message': "name exist",
                                         "success": 0
                                         }, status=200)
                return response
            else:
                hospital = Hospital.objects.create()
                hospital.hospital_auth_code = code
                hospital.name = name
                hospital.created_at = timezone.now()
                hospital.city = city
                hospital.province = province
                hospital.save()
                response = JsonResponse({'message': "register is done",
                                         "success": 0
                                         }, status=200)
                return response
        else:
            response = JsonResponse({'message': "message missed",
                                     "success": 0
                                     }, status=200)
            return response
    else:
        response = JsonResponse({'message': "method not allowed",
                                 "success": 0
                                 }, status=200)
        return response




##成成医院的验证码
def getALLhosoitallist(request):
    if request.method == "GET":
        hospitals = Hospital.objects.all()
        list=[]
        # 遍历所有的 Hospital 对象
        for hospital in hospitals:
            list.append(hospital.name)
        response = JsonResponse({'message': "there are all the hospitals",
                                 "hospital": list
                                 }, status=200)
        return response
    else:
        response = JsonResponse({'message': "method not allowed",
                                 "success": 0
                                 }, status=200)
        return response