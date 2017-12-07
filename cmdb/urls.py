from django.conf.urls import url
from cmdb import views


urlpatterns = [
    url(r'^$', views.AssetListView.as_view(), name='index'),
    url(r'^asset$', views.AssetListView.as_view(), name='asset'),
    url(r'^idc$', views.IdcListView.as_view(), name='idc'),
    url(r'^network$', views.NetworkListView.as_view(), name='network'),
    url(r'^address$', views.IpAddressListView.as_view(), name='address'),
    url(r'^asset/add$', views.AddAssetView.as_view(), name='add_asset'),
]