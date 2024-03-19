from django.db import models
    
class Patient(models.Model):
    GENDER_CHOICES = (
        (0, '未知'),
        (1, '男性'),
        (2, '女性'),
    )

    STATUS_CHOICES = (
        (0, '未激活'),
        (1, '激活'),
    )
    username = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=50)
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    age = models.IntegerField(default =0)
    idCard = models.CharField(max_length=18,default = '')  # 身份证号码一般为18位
    address = models.CharField(max_length=255, default='')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    avatar = models.URLField(default = '')

class Doctor(models.Model):
    email = models.CharField(max_length=25,unique=True)  # 邮箱，假设最大长度为25
    password = models.CharField(max_length=50,default = '')  # 密码，假设最大长度为50
    verification_code = models.CharField(max_length=6)  # 验证码，假设为6位
    verification_code_created_at = models.CharField(max_length=15,default = 0)  #保存验证码的生效起始
    created_at = models.DateTimeField(auto_now_add=True) #账号创建日期
    is_activate = models.BooleanField(default=False)  # 新添加的布尔型字段，默认为False
    token = models.CharField(max_length=50,default = '')


class Hospital(models.Model):
    hospital_auth_id = models.CharField(max_length=10, unique=True)  # 医院独特编号，假设最大长度为10
    province = models.CharField(max_length=50)  # 医院所在省份
    city = models.CharField(max_length=50)  # 医院所在城市
    created_at = models.DateTimeField(auto_now_add=True)  # 医院创建日期