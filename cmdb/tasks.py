from __future__ import absolute_import, unicode_literals

from celery import shared_task
import pepper

from DEVOPS.settings import SALT_API
from cmdb.models import Asset


@shared_task
def add(x, y):
    return x + y


@shared_task
def update_asset_info(asset=None):
    salt_api = pepper.Pepper(SALT_API['url'], ignore_ssl_errors=True)
    salt_api.login(SALT_API['username'], SALT_API['password'], eauth='pam')

    if asset:
        pass
        ret = None
    else:
        ret = salt_api.local('*', 'grains.items')['return'][0]
        print(ret)

    for k, v in ret.items():
        host_type = 0 if v['virtual'] == 'physical' else 1
        ip = None
        Asset.objects.create(hostname=v['host'], asset_type=host_type, vendor=v['manufacturer'],
                             sn=v['serialnumber'], cpu_model=v['cpu_model'], cpu_cores=v['num_cpus'],
                             memory=v['mem_total'], disk_total='100G', disk_info='/', kernel=v['kernel'],
                             kernel_version=v['kernelrelease'], os=v['os'], os_version=v['osrelease'],
                             os_arch=v['osarch'], comment='created from salt.')

    # TODO：更新ip地址，处理资产更新和单资产更新


if __name__ == '__main__':
    update_asset_info()
