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

smtp_server = "smtp.163.com"  # SendGrid SMTP 服务器地址
smtp_port = 465  # SendGrid SMTPS 服务器端口
smtp_username = 'Bravoeye@163.com'
smtp_password = "OXSGUDMRVZOQLIKC"
from_address = "Bravoeye@163.com"



#医生注册发送邮箱
def post_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if email:
            if Doctor.objects.filter(email=email).exists():
                doctor=Doctor.objects.get(email=email)
            else:
                doctor = Doctor(email=email)
                doctor.save()
            code = generate_verification_code()
            doctor.verification_code =code
            doctor.verification_code_created_at = int(time.time())
            doctor.save()
            print("开始发送邮件...")
            email_title = '仁爱之心'
            context = {
                 'code': str(code)
                }
            email_template_name = 'email.html'
            t = loader.get_template(email_template_name)
            html_content = t.render(context)
            # msg = EmailMessage(email_title,
            #         html_content,
            #         settings.EMAIL_HOST_USER,
            #         [email],  # 这里可以同时发给多个收件人
            #         )
            # msg_str = msg.message().as_string()
            try:
                msg = EmailMessage(email_title, html_content, settings.EMAIL_HOST_USER, [email])
                msg.content_subtype = 'html'  # 设置内容类型为HTML
                msg = MIMEText(html_content, 'html', 'utf-8')
                msg['Subject'] = Header(email_title, 'utf-8')
                # 将消息转换为字符串，并指定使用utf-8编码
                # msg.content_subtype = 'html'
                # send_status = msg.send()
                server = smtplib.SMTP_SSL(smtp_server,smtp_port)
                server.login(smtp_username, smtp_password)
                server.sendmail(smtp_username, [email], msg.as_string())
                print("发送邮件成功!")
                return JsonResponse({'message': '请求成功'}, status=200)
            except Exception as e:
                return JsonResponse({'message': 'email is failed'}, status=200)
            finally:
                server.quit()  # 关闭连接
        else:
            return JsonResponse({'message': 'email is empty'}, status=200)
    return JsonResponse({'message': '请求失败'}, status=200)


# 生成邮箱验证码
def generate_verification_code(length=5):
    # 生成包含数字和大写字母的随机验证码
    characters = string.digits + string.ascii_uppercase
    verification_code = ''.join(random.choices(characters, k=length))
    return verification_code


##医生注册界面
def register_doctor(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ######前端的username写的就是email
        email = data.get('username')
        ##############################
        name = data.get('name')
        password = data.get("password")
        verification_code = data.get('verificationCode')
        authCode = data.get("authCode")
        if not Hospital.objects.filter(hospital_auth_code=authCode).exists():
            response = JsonResponse({'message': "authcode is not true"}, status=200)
            return response
        else:
            D_hospital = Hospital.objects.get(hospital_auth_code=authCode)
        print(email, password, verification_code)
        if email and password and verification_code:
            print(2131)
            if Doctor.objects.filter(email=email):
                doctor = Doctor.objects.get(email=email)
            else:
                print(123451121312)
                response = JsonResponse({'message': "Please send the verification code to the email","success":0}, status=200)
                response["message"] = "Please send the verification code to the email"
                response["success"] = 0
                return response
            # 检查是否已经存在该邮箱
            if doctor.is_activate:
                print(12322245)
                response = JsonResponse({'message': "The email has already been registered.","success":0}, status=200)
                response["message"] = "The email has already been registered."
                response["success"] = 0
                return response
            elif doctor.verification_code == verification_code:
                if int(time.time()) - int(doctor.verification_code_created_at) < 300:
                    doctor.password = password
                    doctor.D_hospital = D_hospital.name
                    doctor.name = name
                    doctor.is_activate = True
                    doctor.save()
                else:
                    print(12345233)
                    response = JsonResponse({'message': "Verification code has expired","success":0}, status=200)
                    response["message"] = "Verification code has expired"
                    response["success"] = 0
                    return response
            response = JsonResponse({'message': "Doctor registered successfully","success":1}, status=200)
            response["message"] = "Doctor registered successfully"
            response["success"] = 1
            return response
        else:
            print(12345)
            response = JsonResponse({'message': "message is mis","success":0}, status=200)
            response["message"] = "message is mis"
            response["success"] = 0
            return response
    response = JsonResponse({'message': "Invalid request method","success":0}, status=200)
    response["message"] = "Invalid request method"
    response["success"] = 1
    return response


# 产生token，token有邮箱和时间戳生成
def generate_custom_token(message):
    # timestamp = str(time.time())
    data = message + str(time.time())
    token = hashlib.sha256(data.encode()).hexdigest()
    token = token + "t" + str(int(time.time()))
    return token


# 找到token的时间戳
def get_substring_after_last_occurrence(input_string, char="t"):
    last_index = input_string.rfind(char)

    if last_index != -1 and last_index < len(input_string) - 1:
        substring_after_char = input_string[last_index + 1:]
        return substring_after_char
    else:
        return "未找到字符{}或者{}是最后一个字符".format(char, char)


# 医生登录界面
def doctor_login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("username")
        password = data.get("password")
        if Doctor.objects.filter(email=email):
            doctor = Doctor.objects.get(email=email)
            if doctor.password == password:
                token = generate_custom_token(email)
                if doctor.is_login:
                    doctor.save()
                else:
                    doctor.token = token
                    doctor.is_login = True
                    doctor.save()
                response = JsonResponse(
                    {'message': "password verification successful", "access_token": doctor.token, "id": doctor.id,"success": 1,"name": doctor.name}, status=200)
                response["message"] = "密码登陆成功"
                response["success"] = 1
                response['access_token'] = token
                return response
            # 前端将作为user的cookie作为一个变量保存起来，再下次记录到时，直接登录
            else:
                msg = "password is wrong"
                response = JsonResponse({'message': msg,"success":0}, status=200)
                response["message"] = msg
                response["success"] = 0
                return response
        else:
            msg = "用户名不存在"
    response = JsonResponse({'message': 'please contact to admin',
                             "success": 0
                             }, status=200)
    response["message"] = "django error"
    response["success"] = 0
    return response
