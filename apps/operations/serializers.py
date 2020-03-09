from rest_framework import serializers
from .models import UserFav,UserLeavingMessage,UserAddress
from apps.goods.serializer import GoodsSerializer

class UserFavDetailSerializer(serializers.ModelSerializer):
    good = GoodsSerializer()
    class Meta:
        model = UserFav
        fields = ("good", "id")

class UserFavSerializer(serializers.ModelSerializer):
    #使用当前登录用户作为收藏的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserFav
        fields = ("user", "good", "id")


class UserLeavingMessageSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateField(read_only=True)
    class Meta:
        model = UserLeavingMessage
        fields =("user", "message_type", "subject", "message", "file", "id", "add_time")


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    add_time = serializers.DateField(read_only=True)

    class Meta:
        model = UserAddress
        fields = ("user", "province", "city", "district", "address", "id", "add_time","signer_name","signer_mobile")
