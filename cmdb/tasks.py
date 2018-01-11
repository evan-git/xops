from __future__ import absolute_import, unicode_literals
from datetime import datetime

from celery import shared_task
import pepper

from DEVOPS.settings import SALT_API
from cmdb.models import Asset, IpAddress


@shared_task
def add(x, y):
    return x + y


def _update_asset(obj, v):
    """
    Update asset if asset exists
    :param obj: Asset object
    :param v: single grains return value
    :return:
    """
    host_type = 0 if v['virtual'] == 'physical' else 1
    obj.hostname = v['host']
    obj.asset_type = host_type
    obj.vendor = v['manufacturer']
    obj.sn = v['serialnumber']
    obj.cpu_model = v['cpu_model']
    obj.cpu_cores = v['num_cpus']
    obj.memory = v['mem_total']
    obj.disk_total = '100G'
    obj.disk_info = '/'
    obj.kernel = v['kernel']
    obj.kernel_version = v['kernelrelease']
    obj.os = v['os']
    obj.os_version = v['osrelease']
    obj.os_arch = v['osarch']

    obj.ip.clear()
    for ip in v['ipv4'].remove('127.0.0.1'):
        obj.ip.add(IpAddress.objects.get(ip_address=ip))

    obj.update_date = datetime.now()

    obj.save()


def _create_asset(v):
    """
    Create asset if not exists.
    :param v: single grains return value
    :return:
    """
    host_type = 0 if v['virtual'] == 'physical' else 1
    asset_obj = Asset(hostname=v['host'], asset_type=host_type, vendor=v['manufacturer'],
                      sn=v['serialnumber'], cpu_model=v['cpu_model'], cpu_cores=v['num_cpus'],
                      memory=v['mem_total'], disk_total='100G', disk_info='/', kernel=v['kernel'],
                      kernel_version=v['kernelrelease'], os=v['os'], os_version=v['osrelease'],
                      os_arch=v['osarch'], comment='created from salt.')

    for ip in v['ipv4'].remove('127.0.0.1'):
        asset_obj.ip.add(IpAddress.objects.get(ip_address=ip))

    asset_obj.save()


@shared_task
def update_asset_info(asset=None):
    """
    :param asset: should be list type
    :return: None
    """
    salt_api = pepper.Pepper(SALT_API['url'], ignore_ssl_errors=True)
    salt_api.login(SALT_API['username'], SALT_API['password'], eauth='pam')

    if asset:
        ret = salt_api.local(asset, 'grains.items', expr_form='list')['return'][0]
    else:
        ret = salt_api.local('*', 'grains.items')['return'][0]

    for k, v in ret.items():
        if Asset.objects.filter(sn=v['serialnumber']).exists():
            obj = Asset.objects.get(sn=v['serialnumber'])
            _update_asset(obj, v)
        elif Asset.objects.filter(ip=IpAddress.objects.get(ip_address=k)).exists():
            obj = Asset.objects.get(ip=IpAddress.objects.get(ip_address=k))
            _update_asset(obj, v)
        else:
            _create_asset(v)


if __name__ == '__main__':
    update_asset_info()
