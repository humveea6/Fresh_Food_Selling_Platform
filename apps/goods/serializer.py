from rest_framework import serializers

from apps.goods.models import Goods,GoodsCategory

class GoodsCategorySerializer3(serializers.ModelSerializer):
    """
    商品分类序列化
    """
    class Meta:
        model=GoodsCategory
        fields="__all__"

class GoodsCategorySerializer2(serializers.ModelSerializer):
    """
    商品分类序列化
    """
    sub_cat = GoodsCategorySerializer3(many=True)
    class Meta:
        model=GoodsCategory
        fields="__all__"

class GoodsCategorySerializer(serializers.ModelSerializer):
    """
    商品分类序列化
    """
    sub_cat = GoodsCategorySerializer2(many=True)
    class Meta:
        model=GoodsCategory
        fields="__all__"

class GoodsSerializer(serializers.ModelSerializer):
    """
    商品信息序列化
    """
    category=GoodsCategorySerializer()
    class Meta:
        model=Goods
        fields="__all__"

