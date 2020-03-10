from rest_framework import serializers
from apps.goods.models import Goods
from apps.goods.serializer import GoodsSerializer
from .models import ShoppingCart

class ShopCartDetailSerializer(serializers.ModelSerializer):
    good =GoodsSerializer(many=False)
    class Meta:
        model = ShoppingCart
        fields = "__all__"

class ShopCartSerializer(serializers.Serializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    nums = serializers.IntegerField(required=True,min_value=1,error_messages={
        "min_value":"商品数量最少为1",
        "required":"请填写购买数量"
    })
    good = serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context["request"].user
        nums = validated_data["nums"]
        good = validated_data["good"]

        existed = ShoppingCart.objects.filter(user=user,good=good)
        if existed:
            exist = existed[0]
            exist.nums += nums
            exist.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        #修改商品数量
        instance.nums = validated_data["nums"]
        instance.save()
        return instance
