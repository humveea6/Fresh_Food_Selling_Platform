from rest_framework import mixins,generics,viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filter
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q


from apps.goods.models import Goods,GoodsCategory
from apps.goods.serializer import GoodsSerializer,GoodsCategorySerializer
# Create your views here.

class GoodsFilter(filter.FilterSet):
    """
    商品列表过滤
    """
    pricemin = filter.NumberFilter(field_name="shop_price", lookup_expr='gte')
    pricemax = filter.NumberFilter(field_name="shop_price", lookup_expr='lte')
    #筛选商品类别下面的商品
    top_category = filter.NumberFilter(method='top_category_filter')

    def top_category_filter(self,queryset,name,value):
        queryset = queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))
        return queryset

    class Meta:
        model = Goods
        fields = ['name', 'pricemin', 'pricemax']


class GoodsPagination(PageNumberPagination):
    """
    商品列表自定义分页方式
    """
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100


class GoodsListViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    商品列表页
    """
    # def get(self,request):
    #     goods=Goods.objects.all()[:10]
    #     goods_serializer=GoodsSerializer(goods,many=True)
    #     return Response(goods_serializer.data)
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination
    #自定义字段过滤
    filterset_class=GoodsFilter
    filter_backends = [filters.SearchFilter,DjangoFilterBackend,filters.OrderingFilter]
    #搜索
    search_fields = ['name','goods_desc','goods_brief']
    #排序
    ordering_fields = ['sold_num', 'shop_price']
    #
    # def get(self,request,*args,**kwargs):
    #     return self.list(request,*args,**kwargs)
    #过滤器
    # queryset = Goods.objects.all()
    # def get_queryset(self):
    #     queryset=Goods.objects.all()
        # price_min=self.request.query_params.get("price_min",0)
        # if price_min:
        #     queryset=queryset.filter(shop_price__gt=int(price_min))
        # return queryset


class CategoryViewset(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    """
    queryset = GoodsCategory.objects.all()
    serializer_class = GoodsCategorySerializer