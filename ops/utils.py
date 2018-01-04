import os

import pepper
from django.core.cache import cache
from django.conf import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'DEVOPS.settings'

salt_api = pepper.Pepper(settings.SALT_API['url'], ignore_ssl_errors=True)
salt_api.login(settings.SALT_API['username'], settings.SALT_API['password'], eauth='pam')

ret = salt_api.local('192.168.243.103,192.168.243.1', 'grains.items', expr_form='list')

for k, v in ret['return'][0].items():
    cache.set('grains:%s' % k, v, )


