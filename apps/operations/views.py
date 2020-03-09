from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated
from .models import UserFav,UserLeavingMessage,UserAddress
from .serializers import UserFavSerializer,UserFavDetailSerializer,UserLeavingMessageSerializer,AddressSerializer
from apps.utils.permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.authentication import SessionAuthentication

class UserFavViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    用户收藏
    list:
        获取收藏列表
    retrieve:
        判断商品是否已经收藏
    create:
        收藏商品
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    # serializer_class = UserFavSerializer
    authentication_classes = (JWTAuthentication,SessionAuthentication)
    lookup_field = "good_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer
        else:
            return UserFavSerializer


class UserLeaveMessageViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    用户留言
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    serializer_class = UserLeavingMessageSerializer
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)


class AdressViewset(viewsets.ModelViewSet):
    """
    用户收货地址管理
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication, SessionAuthentication)
    serializer_class = AddressSerializer

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)
