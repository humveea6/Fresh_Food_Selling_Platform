from django.shortcuts import render

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets,status
from rest_framework.response import Response

from apps.users.models import EmailVerifyRecord
from .serializers import EmailSerializer,UserRegisterSerializer
from apps.utils.email import send_email

User=get_user_model()

class CustomBackend(ModelBackend):
    """
    自定义用户登录验证方式
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user=User.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class EmailViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送邮箱验证码
    """
    serializer_class = EmailSerializer

    def create(self, request, *args, **kwargs):
        """
        继承mixins的函数，重写
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email=serializer.validated_data["email"]
        send_status = send_email(email,"register")
        if send_status == False:
            return Response({
                "email":"发送失败！"
            },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "email":email
            },status=status.HTTP_201_CREATED)

        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserViewset(CreateModelMixin,viewsets.GenericViewSet):
    """
    处理用户注册
    """
    serializer_class = UserRegisterSerializer
    #什么作用？
    print("ok2")
    queryset = User.objects.all()
