from django.shortcuts import render
from rest_framework import viewsets,authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import  JWTAuthentication

from apps.utils.permissions import IsOwnerOrReadOnly
from .serializers import ShopCartSerializer,ShopCartDetailSerializer
from .models import ShoppingCart

class ShoppingCartViewset(viewsets.ModelViewSet):
    """
    购物车功能
    """
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JWTAuthentication,authentication.SessionAuthentication)
    # serializer_class = ShopCartSerializer
    lookup_field = "good_id"

    # queryset = ShoppingCart.objects.all()
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)
    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer


