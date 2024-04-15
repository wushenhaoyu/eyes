from datetime import datetime

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
    password = models.CharField(max_length=100, null=True, blank=True)
    verification_code = models.CharField(max_length=6)
    createTime = models.DateTimeField(auto_now_add=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, default=0)
    age = models.IntegerField(default =0)
    idCard = models.CharField(max_length=18,default = '')  # 身份证号码一般为18位
    address = models.CharField(max_length=255, default='')




class MedicalRecords(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    HospitalForTreatment = models.CharField(max_length=15,default="")
    # MedicalRecordTime = models.CharField(max_length=100,default="")
    MedicalRecordTime = models.DateTimeField(db_index=True)
    MedicalRecordStatus = models.BooleanField(default=False)
    MedicalRecordResult = models.CharField(max_length=50,default="")
    VideoName = models.CharField(max_length=255, blank=True, null=True)
    PictureName = models.CharField(max_length=255, blank=True, null=True)



class HistoryRecords(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    HospitalForTreatment = models.CharField(max_length=15,default="")
    # MedicalRecordTime = models.CharField(max_length=100,default="")
    MedicalRecordTime = models.DateTimeField(db_index=True)
    MedicalRecordStatus = models.BooleanField(default=False)
    # Picture = models.ImageField(upload_to='picture/', blank=True, null=True)
    MedicalRecordResult = models.CharField(max_length=50,default="")
    # Video = models.FileField(upload_to='videos/', blank=True, null=True)
    VideoName = models.CharField(max_length=255, blank=True, null=True)
    PictureName = models.CharField(max_length=255, blank=True, null=True)
    DoctorOpinion = models.CharField(max_length=150)
    # VideoLink = models.URLField(max_length=200, blank=True, null=True)
    # PhotoLink = models.URLField(max_length=200, blank=True, null=True)






class Doctor(models.Model):
    name = models.CharField(max_length=25, default="")  # 邮箱，假设最大长度为25
    email = models.CharField(max_length=25,unique=True)  # 邮箱，假设最大长度为25
    password = models.CharField(max_length=50,default = '')  # 密码，假设最大长度为50
    verification_code = models.CharField(max_length=6)  # 验证码，假设为6位
    verification_code_created_at = models.CharField(max_length=15,default = 0)  #保存验证码的生效起始
    created_at = models.DateTimeField(auto_now_add=True) #账号创建日期
    is_activate = models.BooleanField(default=False)  # 新添加的布尔型字段，默认为False
    token = models.CharField(max_length=100,default = '')
    D_hospital = models.CharField(max_length=15, default="")
    is_login = models.BooleanField(default=False)  # 新添加的布尔型字段，默认为False



class Hospital(models.Model):
    hospital_auth_code = models.CharField(max_length=10, unique=True)  # 医院独特验证码
    province = models.CharField(max_length=50)  # 医院所在省份
    city = models.CharField(max_length=50)  # 医院所在城市
    created_at = models.DateTimeField(auto_now_add=True)  # 医院单位创建日期
    name = models.CharField(max_length=50,default = "")


