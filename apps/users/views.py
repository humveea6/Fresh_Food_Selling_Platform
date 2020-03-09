from django.shortcuts import render

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin,UpdateModelMixin
from rest_framework import viewsets,status,permissions,authentication
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import  JWTAuthentication

from apps.users.models import EmailVerifyRecord
from .serializers import EmailSerializer,UserRegisterSerializer,UserDetailSerializer
from apps.utils.email import send_email
from apps.utils.permissions import IsOwnerOrReadOnly

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


class UserViewset(CreateModelMixin,RetrieveModelMixin,viewsets.GenericViewSet,UpdateModelMixin):
    """
    处理用户注册
    """
    # serializer_class = UserRegisterSerializer
    authentication_classes = (authentication.SessionAuthentication, JWTAuthentication)
    #什么作用？
    print("ok2")
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "retrieve" or "update":
            return [permissions.IsAuthenticated()]
        elif self.action == "create":
            return []
        else:
            return []

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegisterSerializer
        else:
            return UserDetailSerializer

    def get_object(self):
        return self.request.user
