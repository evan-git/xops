from django.contrib import admin

from .models import Idc, IpAddress, Network, Asset, AssetGroup


admin.site.register(Idc)
admin.site.register(IpAddress)
admin.site.register(Network)
admin.site.register(Asset)
admin.site.register(AssetGroup)
