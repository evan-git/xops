from django.contrib import admin

from .models import Idc, IpAddress, Network, Asset, AssetGroup


class AssetAdmin(admin.ModelAdmin):
    list_display = ()


class IpAddressAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'is_used', 'is_vip')


admin.site.register(Idc)
admin.site.register(IpAddress, IpAddressAdmin)
admin.site.register(Network)
admin.site.register(Asset)
admin.site.register(AssetGroup)
