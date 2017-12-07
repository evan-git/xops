from django.forms import ModelForm, Select, SelectMultiple
from cmdb import models


class AssetForm(ModelForm):
    class Meta:
        model = models.Asset
        fields = ['sn', 'asset_type', 'ip', 'os', 'group']
        widgets = {
            'asset_type': Select(
                attrs={'class': 'select2'}),
            'group': SelectMultiple(
                attrs={'class': 'select2'}),
            'ip': Select(
                attrs={'class': 'select2'})
        }
