from rest_framework import serializers
from django.contrib.auth import get_user_model
import re
from datetime import datetime,timedelta

from .models import EmailVerifyRecord

User=get_user_model()

class EmailSerializer(serializers.Serializer):
    """
    邮箱验证序列化
    """
    email = serializers.CharField(max_length=150)

    def validate_email(self,email):
        """
        验证邮箱合法性
        :param data:
        :return:
        """
        # print(email)
        #邮箱是否注册
        if User.objects.filter(username=email).count():
            raise serializers.ValidationError("邮箱已被注册！")
        #验证邮箱号码是否合法
        if not re.match("^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$",email):
            raise serializers.ValidationError("邮箱地址不合法！")
        #验证发送频率
        one_min_ago = datetime.now() - timedelta(hours=0,minutes=1,seconds=0)
        if EmailVerifyRecord.objects.filter(email=email,send_time__gt=one_min_ago):
            raise serializers.ValidationError("操作过于频繁！请稍等！")

        return email


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    用户注册验证
    """
    #务必write only！
    code = serializers.CharField(required=True,min_length=8,max_length=8,write_only=True)
    username = serializers.CharField(required=True,allow_blank=False)
    password = serializers.CharField(write_only=True)

    def validate_code(self,code):
        """
        检验验证码
        """
        verify_records = EmailVerifyRecord.objects.filter(email=self.initial_data["username"]).order_by("-send_time")
        if verify_records:
            last_records=verify_records[0]

            five_minutes_ago = datetime.now()-timedelta(hours=0,minutes=5,seconds=0)
            if last_records.send_time < five_minutes_ago:
                raise serializers.ValidationError("验证码过期！")

            if last_records.code != code:
                raise serializers.ValidationError("验证码错误！")
        else:
            raise serializers.ValidationError("验证码错误！")


    def validate_username(self,username):
        """
        检验用户名
        """
        verify_records = EmailVerifyRecord.objects.filter(email=self.initial_data["username"]).order_by("-send_time")
        if verify_records:
            last_records = verify_records[0]

            if last_records.email != username:
                raise serializers.ValidationError("邮箱地址错误！")

            if User.objects.filter(username=username).count():
                raise serializers.ValidationError("用户已存在！")

        else:
            raise serializers.ValidationError("邮箱地址错误！")
        #一定要return username，否则username为空！！！！
        return username

    def validate(self, attrs):
        attrs["email"] = attrs["username"]
        del attrs["code"]
        print("ok1")
        return attrs

    def create(self, validated_data):
        """
        密码加密
        """
        user = super(UserRegisterSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "code","email","password")
