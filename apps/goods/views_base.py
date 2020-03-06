from django.views.generic.base import View
from apps.goods.models import Goods

class GoodsListView(View):
    def get(self,request):
        """
        实现商品列表页
        """
        goods=Goods.objects.all()[:10]
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict=model_to_dict(good)
        #     json_list.append(json_dict)

        import json
        from django.core import serializers
        json_data=serializers.serialize("json",goods)
        print(json_data)
        json_data=json.loads(json_data)

        from django.http import JsonResponse
        return JsonResponse(json_data,safe=False)

