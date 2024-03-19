from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Patient,Doctor
from django.conf import settings
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.generic.base import View
import requests
from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import json
import random
import string
from django.core.mail import EmailMessage
from django.template import loader
import hashlib
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Doctor
from django.core.mail import send_mail


def loginView(request):
    if request.method=="POST":
        phone_number=request.POST.get("phone_number")
        password=request.POST.get("password")
        if Patient.objects.get(phone_number=phone_number):
            patient=Patient.objects.get(phone_number=phone_number)
            if patient.password==password:
                msg="登录成功"
                messages.success(request, "登录成功")
                generate_custom_token(phone_number)
                patient.is_login = True
                return redirect("/index/")
            
            #前端将作为user的cookie作为一个变量保存起来，再下次记录到时，直接登录

            else:       
                msg="用户名密码错误"
        else:
            msg="用户名不存在"
    return render(request,"login.html",locals())        
    # return JsonResponse(
    #             {
    #                 "code": 200,
    #                 "state": -1,
    #                 "msg": msg,

    #             }
    #         )  

#注册
def regView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        phone_number = request.POST.get("phone_number")
        password = request.POST.get("password")
        
        if Patient.objects.filter(phone_number=phone_number).exists():
            msg = "用户名已存在"
            return HttpResponse(msg)
        else:
            # 创建 Patient 对象
            patient = Patient(username=username, phone_number=phone_number, password=password)
            patient.save()
            patient.is_login = True 
            
            #注：前端需要自动登录，否则会报错

            msg = "注册成功"
            return redirect("/login/")
    
    return render(request, "register.html", locals())




def index(request):
    return  render (request,"index.html",{"name":request.session.get('uname')})


def welcome(request):
    return  render (request,"welcome.html",{"name":request.session.get('uname')})





#发送邮箱
def post_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # email = request.POST.get('email')
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
            msg = EmailMessage(email_title, 
                    html_content, 
                    settings.EMAIL_HOST_USER,
                    [email],  # 这里可以同时发给多个收件人
                    )  
            msg.content_subtype = 'html'
            send_status = msg.send()
            print("发送邮件成功!")
            return JsonResponse({'message': '请求成功'}, status=200)
        else:
            return JsonResponse({'message': 'email is empty'}, status=200)
    return JsonResponse({'message': '请求失败'}, status=200)

#生成随机号码
def generate_verification_code(length=5):
    # 生成包含数字和大写字母的随机验证码
    characters = string.digits + string.ascii_uppercase
    verification_code = ''.join(random.choices(characters, k=length))
    return verification_code


##医生注册
def register_doctor(request):
    if request.method == 'POST':
        # email = request.POST.get('email')
        # password = request.POST.get('password')
        # verification_code = request.POST.get('verification_code')
        data = json.loads(request.body)
        # email = request.POST.get('email')
        email = data.get('email')
        password = data.get("password")
        verification_code = data.get('verification_code')
        authcode = data.get("authcode")
        if email and password and verification_code :
            doctor = Doctor.objects.get(email=email)
            # 检查是否已经存在该邮箱
            if doctor.is_activate :
                return JsonResponse({'message': 'Email already exists'}, status=400)
            elif doctor.verification_code == verification_code:
                if int(time.time()) - int(doctor.verification_code_created_at) < 300:
                    doctor.password = password
                    doctor.is_activate = True
                    doctor.save()
                else :
                    return JsonResponse({'message': 'Verification code has expired',
                                         "success" :0
                                         }, status=200)
            return JsonResponse({'message': 'Doctor registered successfully',
                                 "success" :0
                                 }, status=200)

    return JsonResponse({'message': 'Invalid request method',
                         "success": 0 
                         }, status=405)


#产生token，token有邮箱和时间戳生成
def generate_custom_token(message):
    # timestamp = str(time.time())
    data = message + str(time.time())
    token = hashlib.sha256(data.encode()).hexdigest()
    token = token+"t"+str(int(time.time()))
    return token

#找到token的时间戳
def get_substring_after_last_occurrence(input_string, char="t"):
    last_index = input_string.rfind(char)
    
    if last_index != -1 and last_index < len(input_string) - 1:
        substring_after_char = input_string[last_index + 1:]
        return substring_after_char
    else:
        return "未找到字符{}或者{}是最后一个字符".format(char, char)
    
#医生登录
def doctor_login(request):
    if request.method=="POST":
        # phone_number=request.POST.get("phone_number")
        # password=request.POST.get("password")
        data = json.loads(request.body)
        token = data.get("token")
        email = data.get("email")
        password = data.get("password")
        if token and Doctor.objects.get(token = token):
            doctor = Doctor.objects.get(token =token )
            LastLoginTime = int (get_substring_after_last_occurrence(token))
            NowTime = int(time.time())
            if NowTime - LastLoginTime <1209600:
                token = generate_custom_token(email)
                doctor.token = token
                doctor.save()
                return JsonResponse({'message': '登陆成功,token验证成功',
                                        "token":token,
                                        "success":1
                                     }, 
                                    status=200)

        if Doctor.objects.get(email=email):
            doctor=Doctor.objects.get(email=email)
            if doctor.password==password:
                msg="登录成功"
                messages.success(request, "登录成功")
                token = generate_custom_token(email)
                doctor.token = token
                doctor.save()
                return JsonResponse({'message': '密码登陆成功',
                                        "token":token,
                                        "success":1
                                     }, 
                                    status=200)
            
            #前端将作为user的cookie作为一个变量保存起来，再下次记录到时，直接登录

            else:       
                msg="用户名密码错误"
        else:
            msg="用户名不存在"
    return JsonResponse({'message': '无效信息',
                            "success":0
                                     }, 
                                    status=200) 
# if __name__=='__main__':
#    yun_pian=YunPian('***************（你的apikey）')
#    yun_pian.send_sms('***（验证码）','*******（手机号）')

# def view_user_articles(request):
#     if not request.user.is_authenticated:
#         messages.warning(request, "请先登录以访问该页面。")
#         return redirect("/login/")  # 重定向到登录页面
#     user = request.user  # 获取当前登录的用户
#     articles = Article.objects.filter(user=user)  # 获取用户创建的所有文章
#     return render(request, 'user_articles.html', {'articles': articles})

# @login_required
# def write(request):
#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         user = request.user  # 获取当前登录的用户

#         article = Article(title=title, content=content, user=user)
#         article.save()
#         return HttpResponseRedirect('/write/')  # 重定向到文章列表页面或其他适当的页面

#     return render(request, 'write.html', {})





    


# @login_required
# def edit_article(request, article_id):
#     article = get_object_or_404(Article, pk=article_id)

#     if request.method == 'POST':
#         title = request.POST.get('title')
#         content = request.POST.get('content')
#         article.title = title
#         article.content = content
#         article.save()
#         return redirect('view_user_articles')  # 重定向到用户文章列表

#     return render(request, 'edit_article.html', {'article': article})

# def logout_view(request):
#     logout(request)
#     return redirect('/login/')  # 重定向到登录页面，你可以根据你的登录视图的名称进行调整





# def view_published_articles(request):
#     articles = Article.objects.all()  # 获取已发布的文章
#     return render(request, 'published_articles.html', {'articles': articles})



# def view_article(request, article_id):
#     article = get_object_or_404(Article, pk=article_id)
#     return render(request, 'view_article.html', {'article': article})

