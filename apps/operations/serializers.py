from rest_framework import serializers
from .models import UserFav

class UserFavSerializer(serializers.ModelSerializer):
    #使用当前登录用户作为收藏的用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = UserFav
        fields = ("user", "good", "id")
