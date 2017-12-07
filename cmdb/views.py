from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from cmdb import models, forms


class AssetListView(ListView):
    model = models.Asset
    context_object_name = 'assets'
    template_name = 'cmdb/asset.html'


class IpAddressListView(ListView):
    model = models.IpAddress
    context_object_name = 'addresses'
    template_name = 'cmdb/address.html'


class IdcListView(ListView):
    model = models.Idc
    context_object_name = 'idc'
    template_name = 'cmdb/idc.html'


class NetworkListView(ListView):
    model = models.Network
    context_object_name = 'networks'
    template_name = 'cmdb/network.html'


class AddAssetView(CreateView):
    model = models.Asset
    form_class = forms.AssetForm
    success_url = reverse_lazy('cmdb:asset')
    template_name = 'cmdb/add_asset.html'

