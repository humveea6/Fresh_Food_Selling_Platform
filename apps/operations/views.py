from rest_framework import viewsets,mixins
from rest_framework.permissions import IsAuthenticated
from .models import UserFav
from .serializers import UserFavSerializer
from apps.utils.permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import  JWTAuthentication
from rest_framework.authentication import SessionAuthentication

class UserFavViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    用户收藏
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    serializer_class = UserFavSerializer
    authentication_classes = (JWTAuthentication,SessionAuthentication)
    lookup_field = "good_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)