from django.contrib import messages
from .models import Patient, Doctor, Hospital,MedicalRecords,HistoryRecords
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
        print(username, password, gender, age, idCard)
        print(idCard, phone_number, address, adminpassword)

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


# def save_media(request):
#     if request.method == 'POST':
#         hospital = request.POST.get('hospital')
#         record_time = request.POST.get('check_time')
#         picture_file = request.FILES.get('eyeUserFile_resuiltImage')
#         video_file = request.FILES.get('checkVideoPath')
#         record_result = request.POST.get('predict')
#         phone_number = request.POST.get('phone_number')
#         patient = Patient.objects.get(phone_number=phone_number)
#         if hospital == '':
#             hospital = "王浩宇医院"
#         # 创建 MedicalRecords 实例并保存视频和照片文件
#         medical_record = MedicalRecords(patient=patient, HospitalForTreatment=hospital,
#                                         MedicalRecordTime=record_time, MedicalRecordResult=record_result)
#         # 保存照片文件
#         if picture_file:
#             medical_record.Picture = picture_file
#             print(1)
#         # 保存视频文件
#         if video_file:
#             medical_record.Video = video_file
#         medical_record.save()
#         response = JsonResponse({'message': "okoksuccess",
#                                  "success": 1
#                                  }, status=200)
#         return response
#     else:
#         response = JsonResponse({'message': "method not allowed",
#                                  "success": 0
#                                  }, status=200)
#         return response
#

import requests
import uuid
import os

def download_and_save_file(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)


def save_media(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        hospital = data.get("hospital")
        print(hospital)
        record_time = data.get("check_time")
        unique_filename = str(uuid.uuid4())
        picture_url = data.get("resultImage")
        print(picture_url)
        picture_save_path = 'picture/images/' + unique_filename+'.png'
        try:
            download_and_save_file(picture_url, picture_save_path)
        except Exception as e:
            print(e)
            response = JsonResponse({'message': "picture is missing"})
            return response

        # 下载并保存视频文件或链接
        video_url = data.get("checkVideoPath")
        video_save_path = 'picture/' + unique_filename+'.mp4'  # 保存视频的路径
        try:
            download_and_save_file(video_url, video_save_path)
        except Exception as e:
            print(e)
            response = JsonResponse({'message': "photo is missing"})
            return response


        record_result = data.get('predict')

        phone_number = data.get('phone_number')
        patient = Patient.objects.get(phone_number=phone_number)
        # 创建医疗记录对象并保存到数据库
        medical_record = MedicalRecords(patient=patient, HospitalForTreatment=hospital,
                                        MedicalRecordTime=record_time, MedicalRecordResult=record_result)

        # 保存图片和视频文件或链接的路径到对应字段
        medical_record.PictureName = unique_filename+'.png'
        medical_record.VideoName = unique_filename+'.mp4'


        # 保存视频和图片的链接到对应字段


        medical_record.save()
        response = JsonResponse({'message':"okok"})
        return response
    else:
        unique_filename = str(uuid.uuid4())
        picture_save_path = 'picture/images/' + unique_filename + '.png'
        response = JsonResponse({'message': picture_save_path})
        return response


def update_patinet_message(request):
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
        print(username, password, gender, age, idCard)
        print(idCard, phone_number, address, adminpassword)
        if(adminpassword =="Bravo"):
            patient = Patient.objects.get(phone_number=phone_number)

            # Update patient information
            patient.username = username
            patient.password = password
            patient.gender = gender
            patient.age = age
            patient.phone_number = phone_number
            patient.address = address
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



import re


def change_hospital(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        hospital = data.get("hospital")
        phone_number = data.get("phone")
        MedicalRecordTime1 = data.get("date")

        # 解析不包含秒的日期时间字符串
        MedicalRecordTime = datetime.strptime(MedicalRecordTime1, "%Y-%m-%dT%H:%M:%S")
        print(MedicalRecordTime)



        specific_medical_records = MedicalRecords.objects.filter(patient__phone_number=phone_number,
                                                                 MedicalRecordTime=MedicalRecordTime)
        if not specific_medical_records:
            specific_medical_record = HistoryRecords.objects.get(patient__phone_number=phone_number, MedicalRecordTime=MedicalRecordTime)
            specific_medical_record.HospitalForTreatment = hospital
        else:
            specific_medical_record = MedicalRecords.objects.get(patient__phone_number=phone_number, MedicalRecordTime=MedicalRecordTime)
            specific_medical_record.HospitalForTreatment = hospital
        specific_medical_record.save()
        response = JsonResponse({'message': "修改完毕"})
        return response
    else:
        response = JsonResponse({'message': "method not allowed"})
        return response