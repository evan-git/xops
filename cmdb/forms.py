from django.forms import ModelForm, Select, SelectMultiple
from cmdb import models


class AssetForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(AssetForm, self).__init__(*args, **kwargs)
        # self.fields['ip'].queryset = models.IpAddress.objects.filter(is_used=False)
        self.fields['ip'].queryset = [obj for obj in models.IpAddress.objects.all() if not obj.is_used]

    class Meta:
        model = models.Asset
        fields = ['hostname', 'asset_type', 'ip', 'group', 'cpu_cores', 'memory']
        widgets = {
            'asset_type': Select(
                attrs={'class': 'select2'}),
            'group': SelectMultiple(
                attrs={'class': 'select2'})
        }

    def clean_ip(self):
        ip = self.cleaned_data.get("ip")
        if models.IpAddress.objects.get(ip_address=ip).asset_set.count() != 0 or \
                not models.IpAddress.objects.filter(ip_address=ip).exists():
            raise ValidationError('Ip already used or not exists.')
        return models.IpAddress.objects.get(ip_address=ip)
