"""FreshShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.views.static import serve
import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter

from FreshShop import settings
from apps.goods.views import GoodsListViewset,CategoryViewset


router = DefaultRouter()

#商品列表url
router.register(r'goods',GoodsListViewset,basename="Goods")


#商品分类url
router.register(r'categorys',CategoryViewset,basename="GoodsCategory")

urlpatterns = [
    #router相关
    path('', include(router.urls)),
    #admin页面
    path('admin/', xadmin.site.urls),
    #上传文件访问URL
    re_path('media/(?P<path>.*)$',serve,{"document_root":settings.MEDIA_ROOT}),

    # #商品详情页
    # re_path("goods/$",goods_list,name="goods_list"),

    path("docs/",include_docs_urls(title="生鲜商城")),

    re_path(r'^api-auth/', include('rest_framework.urls')),
]
