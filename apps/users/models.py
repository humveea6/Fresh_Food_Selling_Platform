from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class BaseModel(models.Model):
    """
    基础model，主要是增加时间
    """
    add_time=models.DateField(default=datetime.now,verbose_name="添加时间")


class UserProfile(AbstractUser):
    """
    用户信息
    """
    name=models.CharField(max_length=30,null=True,blank=True,verbose_name="姓名")
    birthday=models.DateField(null=True,blank=True,verbose_name="出生日期")
    mobile=models.CharField(max_length=11,verbose_name="手机号码",null=True,blank=True)
    gender=models.CharField(max_length=6,choices=(("male","男"),("female","女")),verbose_name="性别",default="female")
    email=models.EmailField(max_length=150,null=True,blank=True,verbose_name="邮箱")

    class Meta:
        verbose_name="用户信息"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    短信验证码
    """
    code=models.CharField(max_length=20,verbose_name="验证码")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    add_time = models.DateField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name="短信验证码"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.mobile


class EmailVerifyRecord(models.Model):
    code=models.CharField(max_length=20,verbose_name="邮箱验证码")
    email=models.EmailField(max_length=150,verbose_name="邮箱地址")
    send_type=models.CharField(verbose_name="验证码类型",choices=(("register","注册"),("forget","找回")),max_length=8)
    send_time=models.DateTimeField(verbose_name="发送时间",default=datetime.now)

    class Meta:
        verbose_name="邮箱验证码"
        verbose_name_plural=verbose_name


    def __str__(self):
        return "{}({})".format(self.code,self.email)