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
from django.shortcuts import render
from django.http import JsonResponse
import smtplib
from email.mime.text import MIMEText
def index_vue(request):
    return render(request, 'index.html')
def get_substring_after_last_occurrence(input_string, char="t"):
    last_index = input_string.rfind(char)

    if last_index != -1 and last_index < len(input_string) - 1:
        substring_after_char = input_string[last_index + 1:]
        return substring_after_char
    else:
        return "未找到字符{}或者{}是最后一个字符".format(char, char)
##检查是否登录
def is_login(token):
    if token and Doctor.objects.filter(token=token):
        LastLoginTime = int(get_substring_after_last_occurrence(token))
        NowTime = int(time.time())
        if NowTime - LastLoginTime < 1209600:
            return True
        else:
            return False
    else:
        return False


##
def gender(request):
    return JsonResponse(
        {
            "code": 200,
            "data": [
                {
                    "genderLabel": "男",
                    "genderValue": 1
                },
                {
                    "genderLabel": "女",
                    "genderValue": 2
                }
            ],
            "msg": "get success"
        }
    )

def test(request):
    patient = Patient.objects.get(id=1)

    # 创建一个 MedicalRecords 对象
    medical_record = MedicalRecords.objects.get(id=1)

    return JsonResponse(
        {
            "code": medical_record.MedicalRecordTime
        }
    )



#############待诊治患者
def getUserList(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token = request.headers.get('X-Access-Token', '')
        if not is_login(token):
            print(123)
            response = JsonResponse({'message': "please login first", "success": 0}, status=401)
            response["code"] = 401
            return response
        else:
            doctor = Doctor.objects.get(token=token)
            hospital = doctor.D_hospital
            print(123)
            pageNum = data.get("pageNum")
            pageSize = data.get("pageSize")
            gender = (data.get("gender"))
            idCard = (data.get("idCard"))
            maxAge = (data.get("maxAge"))
            minAge = (data.get("minAge"))
            username = data.get("username")
            startTime_str = data.get("startTime")
            endTime_str = data.get("endTime")
            startTime = datetime.strptime(startTime_str, '%Y-%m-%d %H:%M:%S')
            endTime = datetime.strptime(endTime_str, '%Y-%m-%d %H:%M:%S')
            # 构建查询条件
            filters = {}
            if gender:
                gender = int(data.get("gender"))
                filters['patient__gender'] = gender
            if idCard:
                filters['patient__idCard'] = idCard
            if maxAge:
                maxAge = int(data.get("maxAge"))
                filters['patient__age__lte'] = maxAge
            if minAge:
                minAge = int(data.get("minAge"))
                filters['patient__age__gte'] = minAge
            if username:
                filters['patient__username__icontains'] = username
            if startTime and endTime:
                filters['MedicalRecordTime__range'] = [startTime, endTime]
            if hospital:
                filters['HospitalForTreatment'] = hospital
            print(filters)
            start = pageSize * (pageNum - 1)
            end = start + pageSize-1
            print(start,end)
            recent_patients = MedicalRecords.objects.filter(**filters).order_by('-MedicalRecordTime')[start:end]
            total = MedicalRecords.objects.filter(**filters).count()
            list = []
            if recent_patients:
                for recent_patient in recent_patients:
                    formatted_patient = {
                        "id": recent_patient.id,
                        "username": recent_patient.patient.username,
                        "gender": recent_patient.patient.gender,
                        "user": {
                            "detail": {
                                "age": recent_patient.patient.age
                            }
                        },
                        "idCard": recent_patient.patient.idCard,
                        "email": recent_patient.patient.phone_number,
                        "address": recent_patient.patient.address,
                        "createTime": recent_patient.MedicalRecordTime,
                        "status": recent_patient.MedicalRecordStatus,
                        "avatar": 1
                    }
                    list.append(formatted_patient)

                response_data = {
                    "code": 200,
                    "msg": "成功",
                    "data": {
                        "list": list,
                        "pageSize": pageSize,
                        "pageNum":pageNum,
                        "total":total
                    }
                }
                response = JsonResponse(response_data, status=200)
                return response
            else:
                response_data = {
                    "code": 200,
                    "msg": "失败",
                    "data": {
                        "list": [],
                        "pageSize": pageSize,
                        "pageNum": pageNum,
                        "total": total
                    }
                }
                response = JsonResponse(response_data, status=200)
                return response
    else:
        response = JsonResponse({'message': "method not allowed", "success": 0}, status=200)
        return response



#############历史患者
def getHistoryUserList(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token = request.headers.get('X-Access-Token', '')
        if not is_login(token):
            response = JsonResponse({'message': "please login first", "success": 0}, status=401)
            response["code"] = 401
            return response
        else:
            doctor = Doctor.objects.get(token=token)
            hospital = doctor.D_hospital
            pageNum = data.get("pageNum")
            pageSize = data.get("pageSize")
            gender = (data.get("gender"))
            idCard = (data.get("idCard"))
            maxAge = (data.get("maxAge"))
            minAge = (data.get("minAge"))
            username = data.get("username")
            startTime_str = data.get("startTime")
            endTime_str = data.get("endTime")
            startTime = datetime.strptime(startTime_str, '%Y-%m-%d %H:%M:%S')
            endTime = datetime.strptime(endTime_str, '%Y-%m-%d %H:%M:%S')
            # 构建查询条件
            filters = {}
            if gender:
                gender = int(data.get("gender"))
                filters['patient__gender'] = gender
            if idCard:
                filters['patient__idCard'] = idCard
            if maxAge:
                maxAge = int(data.get("maxAge"))
                filters['patient__age__lte'] = maxAge
            if minAge:
                minAge = int(data.get("minAge"))
                filters['patient__age__gte'] = minAge
            if username:
                filters['patient__username__icontains'] = username
            if startTime and endTime:
                filters['MedicalRecordTime__range'] = [startTime, endTime]
            if hospital:
                filters['HospitalForTreatment'] = hospital
            print(filters)
            start = pageSize * (pageNum - 1)
            end = start + pageSize-1
            print(start,end)
            recent_patients = HistoryRecords.objects.filter(**filters).order_by('-MedicalRecordTime')[start:end]
            total = HistoryRecords.objects.filter(**filters).count()
            list = []
            if recent_patients:
                for recent_patient in recent_patients:
                    print(recent_patient.id)
                    formatted_patient = {
                        "id": recent_patient.id,
                        "username": recent_patient.patient.username,
                        "gender": recent_patient.patient.gender,
                        "user": {
                            "detail": {
                                "age": recent_patient.patient.age
                            }
                        },
                        "idCard": recent_patient.patient.idCard,

                        "email": recent_patient.patient.phone_number,
                        "address": recent_patient.patient.address,
                        "createTime": recent_patient.MedicalRecordTime,
                        "status": recent_patient.MedicalRecordStatus,
                        "avatar": 1
                    }
                    list.append(formatted_patient)

                response_data = {
                    "code": 200,
                    "msg": "成功",
                    "data": {
                        "list": list,
                        "pageSize": pageSize,
                        "pageNum":pageNum,
                        "total":total
                    }
                }
                response = JsonResponse(response_data, status=200)
                return response
            else:
                response_data = {
                    "code": 200,
                    "msg": "失败",
                    "data": {
                        "list": [],
                        "pageSize": pageSize,
                        "pageNum": pageNum,
                        "total": total
                    }
                }
                response = JsonResponse(response_data, status=200)
                return response
    else:
        response = JsonResponse({'message': "method not allowed", "success": 0}, status=200)
        return response


def PatientAdvice(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        phone_number = data.get('email')
        MedicalRecordTime = data.get('createTime')
        advice = data.get('advice')
        medical_recordss = MedicalRecords.objects.filter(patient__phone_number=phone_number,MedicalRecordTime=MedicalRecordTime)
        medical_record=medical_recordss[0]
        if medical_record:
            history_record = HistoryRecords(
                patient=medical_record.patient,
                HospitalForTreatment=medical_record.HospitalForTreatment,
                MedicalRecordTime=medical_record.MedicalRecordTime,
                MedicalRecordStatus=medical_record.MedicalRecordStatus,
                PictureName=medical_record.PictureName,
                VideoName=medical_record.VideoName,
                MedicalRecordResult=medical_record.MedicalRecordResult,
                DoctorOpinion=advice  # 使用从请求中获取的 advice 作为 DoctorOpinion
            )
            history_record.save()  # 保存新的 HistoryRecords 记录
            medical_record.delete()
        response = JsonResponse({'message': "success", "success": 1}, status=200)
        return response









def geturl(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token = request.headers.get('X-Access-Token', '')
        id = data.get('id')
        print(data)
        if not is_login(token):
            response = JsonResponse({'message': "please login first", "success": 0}, status=401)
            response["code"] = 401
            return response
        else:
            print(123)
            specific_medical_records = MedicalRecords.objects.filter(id=id)
            print(specific_medical_records)
            if not specific_medical_records:
                print(id)
                specific_medical_record =HistoryRecords.objects.get(id=id)
                print(specific_medical_record.VideoName)
                video_path = "https://nwpu.space:82/"+specific_medical_record.VideoName
                picture_path = "https://nwpu.space:82/images/"+specific_medical_record.PictureName
                Advice = specific_medical_record.DoctorOpinion
            else:
                specific_medical_record = MedicalRecords.objects.get(id=id)
                video_path = "https://nwpu.space:82/" + specific_medical_record.VideoName
                picture_path = "https://nwpu.space:82/images/" + specific_medical_record.PictureName
                Advice = None
            if specific_medical_record.MedicalRecordResult[0] == "N":
                result = "无症状"
            elif specific_medical_record.MedicalRecordResult[0] == "L":
                result = "左跳型眼震"
            else:
                result = "右跳型眼震"





            response = JsonResponse({'video': video_path,'picture': picture_path, "result":result ,"Advice": Advice}, status=200)
            return response

    else:
        response = JsonResponse({'message': "method not allowed", "success": HistoryRecords.objects.get(id=id)}, status=200)
        return response




#############历史患者
def getALLUserList(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token = request.headers.get('X-Access-Token', '')
        if not is_login(token):
            response = JsonResponse({'message': "please login first", "success": 0}, status=401)
            response["code"] = 401
            return response
        else:
            doctor = Doctor.objects.get(token=token)
            pageNum = data.get("pageNum")
            pageSize = data.get("pageSize")
            gender = (data.get("gender"))
            maxAge = (data.get("maxAge"))
            minAge = (data.get("minAge"))
            startTime_str = data.get("startTime")
            endTime_str = data.get("endTime")
            startTime = datetime.strptime(startTime_str, '%Y-%m-%d %H:%M:%S')
            endTime = datetime.strptime(endTime_str, '%Y-%m-%d %H:%M:%S')
            # 构建查询条件
            filters = {}
            if gender:
                gender = int(data.get("gender"))
                filters['patient__gender'] = gender
            if maxAge:
                maxAge = int(data.get("maxAge"))
                filters['patient__age__lte'] = maxAge
            if minAge:
                minAge = int(data.get("minAge"))
                filters['patient__age__gte'] = minAge
            if startTime and endTime:
                filters['MedicalRecordTime__range'] = [startTime, endTime]
            print(filters)
            start = pageSize * (pageNum - 1)
            end = start + pageSize-1
            print(start,end)
            recent_patients = HistoryRecords.objects.filter(**filters).order_by('-MedicalRecordTime')[start:end]
            total = HistoryRecords.objects.filter(**filters).count()
            list = []
            if recent_patients:
                for recent_patient in recent_patients:
                    print(recent_patient.id)
                    formatted_patient = {
                        "id": recent_patient.id,
                        "gender": recent_patient.patient.gender,
                        "user": {
                            "detail": {
                                "age": recent_patient.patient.age
                            }
                        },
                        "createTime": recent_patient.MedicalRecordTime,
                    }
                    list.append(formatted_patient)
                response_data = {
                    "code": 200,
                    "msg": "成功",
                    "data": {
                        "list": list,
                        "pageSize": pageSize,
                        "pageNum":pageNum,
                        "total":total
                    }
                }
                response = JsonResponse(response_data, status=200)
                return response
            else:
                response_data = {
                    "code": 200,
                    "msg": "失败",
                    "data": {
                        "list": [],
                        "pageSize": pageSize,
                        "pageNum": pageNum,
                        "total": total
                    }
                }
                response = JsonResponse(response_data, status=200)
                return response
    else:
        response = JsonResponse({'message': "method not allowed", "success": 0}, status=200)
        return response
